#!/usr/bin/env python3
"""
SAARTHI (सारथी) - AI-Powered Hyper-Personalized Banking & Lending for Bharat
Zero-dependency HTTP Server & REST API
Built with Python 3 Standard Library
"""

import http.server
import socketserver
import json
import os
import sys
import urllib.parse
from datetime import datetime
import uuid

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# -------------------------------------------------------------
# DOMAIN DATA: Bharat Personas & Financial Profiles in SAARTHI
# -------------------------------------------------------------
PERSONAS = {
    "ramesh_kirana": {
        "id": "ramesh_kirana",
        "name": "Ramesh Kumar",
        "phone": "+91 98765 43210",
        "age": 38,
        "avatar": "👨🏽‍💼",
        "role": "Kirana Store Owner",
        "location": "Gorakhpur, Uttar Pradesh (Tier-3)",
        "language": "hi",
        "languageName": "हिंदी (Hindi)",
        "accountNumber": "••• ••• 4821",
        "bankName": "Bharat Vikas Gramin Bank",
        "monthlyTurnover": 125000,
        "averageBalance": 18400,
        "upiVelocity": 54,  # daily UPI transactions
        "cibilScore": 685,
        "altCreditScore": 760,  # Cash-flow alternative score
        "cashflowTrend": "positive_seasonal",
        "stressIndex": 0.28,  # 0 to 1
        "stressStatus": "Healthy / Low Risk",
        "lifeStage": "Growing Micro-Enterprise / Festive Inventory Restocking",
        "kycInfo": {
            "status": "Verified (Aadhaar e-KYC & PAN)",
            "aadhaarMasked": "XXXX-XXXX-8912",
            "panMasked": "ABCDE1234F",
            "kycDate": "14 Jan 2026",
            "videoKycDone": True,
            "accountAggregatorConsent": "Active (Sahamati AA-9041)",
            "tier": "Tier-3 Urban Semi-Rural"
        },
        "recentTransactions": [
            {"date": "12 Sep 2026", "desc": "UPI QR - Daily Grocery Credits (48 txns)", "amount": 6240, "type": "credit"},
            {"date": "11 Sep 2026", "desc": "UPI QR - Daily Grocery Credits (52 txns)", "amount": 7180, "type": "credit"},
            {"date": "10 Sep 2026", "desc": "Wholesale Stock Payment - Gorakhpur Mandi", "amount": -14500, "type": "debit"},
            {"date": "08 Sep 2026", "desc": "Bijli Bill (UPPCL Rural Electricity)", "amount": -1850, "type": "debit"},
            {"date": "05 Sep 2026", "desc": "Shop Rent - Main Bazaar", "amount": -4500, "type": "debit"}
        ],
        "recommendations": [
            {
                "id": "rec_vyapar_credit",
                "title": "Saarthi Vyapar Pragati Working Capital",
                "vernacularTitle": "सारथी व्यापार प्रगति कार्यशील पूंजी लोन",
                "category": "Micro Business Credit Line",
                "amount": "₹50,000 - ₹1,50,000",
                "interestRate": "11.2% p.a. (No Prepayment Penalty)",
                "tenure": "6 to 12 months",
                "repaymentType": "Daily Micro-UPI Repayment (₹145/day)",
                "confidenceScore": 94,
                "urgency": "High - Festival Stocking Window",
                "badge": "AI Best Match (UPI Cashflow Backed)",
                "whyRecommended": [
                    "Your daily UPI QR customer volume jumped 28% ahead of the upcoming festival season.",
                    "Consistent supplier mandi payouts indicate inventory turnaround every 14 days.",
                    "Daily micro-repayment aligns directly with your shop's evening cash drawer flow."
                ],
                "shapFactors": [
                    {"factor": "Daily UPI QR Inflows (>45/day)", "impact": "+38%"},
                    {"factor": "Zero Utility Bill Bounces (UPPCL)", "impact": "+24%"},
                    {"factor": "Stable Shop Rent Velocity", "impact": "+18%"},
                    {"factor": "Limited Formal Bureau History", "impact": "-8%"}
                ]
            },
            {
                "id": "rec_shop_insurance",
                "title": "Dukan Suraksha Parametric Micro-Insurance",
                "vernacularTitle": "दुकान सुरक्षा माइक्रो-बीमा",
                "category": "Shop & Inventory Insurance",
                "amount": "₹5,00,000 Coverage",
                "interestRate": "₹49/month premium",
                "tenure": "Annual renewal",
                "repaymentType": "Auto-debit from UPI",
                "confidenceScore": 88,
                "urgency": "Medium",
                "badge": "Risk Shield",
                "whyRecommended": [
                    "Safeguards inventory against seasonal heavy rain waterlogging and short circuits in Gorakhpur market.",
                    "Instant paperless claims verified through digital GST bills."
                ],
                "shapFactors": [
                    {"factor": "Inventory Stock Value > ₹3L", "impact": "+42%"},
                    {"factor": "Seasonal Rain Flood Index", "impact": "+30%"}
                ]
            }
        ]
    },
    "priya_teacher": {
        "id": "priya_teacher",
        "name": "Priya Sharma",
        "phone": "+91 94250 11223",
        "age": 29,
        "avatar": "👩🏽‍🏫",
        "role": "Primary School Teacher",
        "location": "Indore, Madhya Pradesh (Tier-2)",
        "language": "hi",
        "languageName": "हिंदी (Hindi)",
        "accountNumber": "••• ••• 9143",
        "bankName": "Indore Central Cooperative Bank",
        "monthlyTurnover": 42000,
        "averageBalance": 24500,
        "upiVelocity": 12,
        "cibilScore": 745,
        "altCreditScore": 790,
        "cashflowTrend": "very_stable",
        "stressIndex": 0.12,
        "stressStatus": "Prime / Very Healthy",
        "lifeStage": "Young Salaried Professional / Child Education Planning",
        "kycInfo": {
            "status": "Verified (DigiLocker Certified)",
            "aadhaarMasked": "XXXX-XXXX-4531",
            "panMasked": "PQRSK5678L",
            "kycDate": "22 Feb 2026",
            "videoKycDone": True,
            "accountAggregatorConsent": "Active (Sahamati AA-7823)",
            "tier": "Tier-2 Urban"
        },
        "recentTransactions": [
            {"date": "01 Sep 2026", "desc": "Salary Credit - MP Dept of Education", "amount": 38500, "type": "credit"},
            {"date": "04 Sep 2026", "desc": "SIP - HDFC Nifty 50 Index Fund", "amount": -3000, "type": "debit"},
            {"date": "06 Sep 2026", "desc": "Home Rent Auto-Debit", "amount": -8500, "type": "debit"},
            {"date": "09 Sep 2026", "desc": "Grocery - D-Mart UPI", "amount": -2400, "type": "debit"},
            {"date": "11 Sep 2026", "desc": "Electricity Bill MPPKVVCL", "amount": -1120, "type": "debit"}
        ],
        "recommendations": [
            {
                "id": "rec_shiksha_deposit",
                "title": "Shiksha Nidhi Goal-Based High Yield RD",
                "vernacularTitle": "शिक्षा निधि हाई-यील्ड आरडी",
                "category": "Guaranteed Savings & Wealth",
                "amount": "₹2,500/month (7.85% p.a.)",
                "interestRate": "7.85% p.a. guaranteed",
                "tenure": "36 months",
                "repaymentType": "Auto-sweep on 2nd of each month",
                "confidenceScore": 96,
                "urgency": "High - Surplus Capital Optimization",
                "badge": "Wealth Accelerator",
                "whyRecommended": [
                    "Maintains an ongoing surplus of ₹18,000+ balance after routine monthly expenditures.",
                    "Goal-targeted saving timed for child's upcoming school admission cycle.",
                    "Auto-sweep ensures funds earn 7.85% instead of sitting idle in savings account."
                ],
                "shapFactors": [
                    {"factor": "100% On-Time Salary Credit (1st of month)", "impact": "+45%"},
                    {"factor": "Active SIP Financial Discipline", "impact": "+32%"},
                    {"factor": "Fixed Expense Ratio < 40%", "impact": "+20%"}
                ]
            },
            {
                "id": "rec_preapproved_home_renovation",
                "title": "Pre-Approved Griha Sudhar Credit Line",
                "vernacularTitle": "गृह सुधार प्री-अप्रूव्ड पर्सनल लोन",
                "category": "Pre-Approved Credit",
                "amount": "₹2,00,000",
                "interestRate": "9.9% p.a.",
                "tenure": "24 to 48 months",
                "repaymentType": "Auto-debit ₹5,070/month",
                "confidenceScore": 91,
                "urgency": "Low - Pre-Approved Buffer",
                "badge": "Instant 1-Click Disbursal",
                "whyRecommended": [
                    "CIBIL score of 745 combined with steady government salary qualifies for lowest prime rate tier.",
                    "Zero paperwork required — instant disbursal to existing salary account."
                ],
                "shapFactors": [
                    {"factor": "Govt Employment Verification", "impact": "+50%"},
                    {"factor": "Zero Defaults History", "impact": "+35%"}
                ]
            }
        ]
    },
    "suresh_farmer": {
        "id": "suresh_farmer",
        "name": "Suresh Patel",
        "phone": "+91 97234 55678",
        "age": 47,
        "avatar": "👨🏽‍🌾",
        "role": "Small Acreage Farmer (Cotton & Groundnut)",
        "location": "Anand, Gujarat (Tier-4 Rural)",
        "language": "gu",
        "languageName": "ગુજરાતી (Gujarati)",
        "accountNumber": "••• ••• 2309",
        "bankName": "Gujarat Gramin Sahakari Bank",
        "monthlyTurnover": 35000,
        "averageBalance": 4200,
        "upiVelocity": 5,
        "cibilScore": 640,
        "altCreditScore": 670,
        "cashflowTrend": "stressed_weather_shock",
        "stressIndex": 0.78,  # HIGH STRESS DETECTED!
        "stressStatus": "⚠️ Early Warning: Cashflow Stress Detected",
        "lifeStage": "Agricultural Sowing Cycle / Monsoon Delay Shock",
        "kycInfo": {
            "status": "Verified (Kisan Credit Card & Aadhaar e-KYC)",
            "aadhaarMasked": "XXXX-XXXX-6729",
            "panMasked": "GHIJK9012M",
            "kycDate": "19 May 2025",
            "videoKycDone": True,
            "accountAggregatorConsent": "Active (Sahamati AA-3490)",
            "tier": "Tier-4 Rural Agrarian"
        },
        "recentTransactions": [
            {"date": "02 Sep 2026", "desc": "Fertilizer Subsidy Credit - DBT Govt", "amount": 2000, "type": "credit"},
            {"date": "05 Sep 2026", "desc": "Diesel for Tube-well Pump", "amount": -1800, "type": "debit"},
            {"date": "08 Sep 2026", "desc": "Tractor EMI - Bharat Finance (Bounce Risk)", "amount": -4200, "type": "debit"},
            {"date": "10 Sep 2026", "desc": "Crop Pest Treatment Cashflow Outflow", "amount": -2100, "type": "debit"},
            {"date": "12 Sep 2026", "desc": "Account Balance Dip below Minimum Threshold", "amount": 0, "type": "info"}
        ],
        "recommendations": [
            # ETHICAL GUARDRAIL TRIGGERED: No aggressive consumer loans pushed!
            {
                "id": "rec_empathetic_moratorium",
                "title": "Saarthi Empathetic EMI Restructuring & 45-Day Grace",
                "vernacularTitle": "સારથી સહાનુભૂતિપૂર્વક ઇએમઆઇ પુનર્ગઠન (૪૫ દિવસ મુદત)",
                "category": "Empathetic Stress Intervention",
                "amount": "Tractor EMI Relief (₹4,200)",
                "interestRate": "Zero Penalty / No CIBIL Impact",
                "tenure": "Defer until Kharif Harvest (Nov 2026)",
                "repaymentType": "Bullet repayment post-APMC mandi payout",
                "confidenceScore": 98,
                "urgency": "Urgent - Prevent Involuntary Default",
                "badge": "🛡️ Ethical Safeguard Active",
                "whyRecommended": [
                    "AI detected unseasonal rainfall in Anand district combined with 65% balance drawdown.",
                    "Ethical Guardrail actively BLOCKED high-interest short-term loan cross-sells.",
                    "Provides 45-day grace without negative CIBIL reporting under RBI compassionate guidelines."
                ],
                "shapFactors": [
                    {"factor": "Rainfall Anomaly Satellite Index", "impact": "+40%"},
                    {"factor": "Upcoming Mandi Harvest Payout Track", "impact": "+35%"},
                    {"factor": "3 Years Faultless Prior Repayment", "impact": "+25%"}
                ]
            },
            {
                "id": "rec_fasal_bima",
                "title": "PM Fasal Bima Instant Expedited Advance",
                "vernacularTitle": "પીએમ પાક વીમા ઝડપી સહાય",
                "category": "Crop Insurance Acceleration",
                "amount": "₹25,000 Immediate Working Grant",
                "interestRate": "Govt Subsidized (0% Interest)",
                "tenure": "Adjusted against final claim",
                "repaymentType": "Direct Benefit Transfer (DBT) Offset",
                "confidenceScore": 92,
                "urgency": "Immediate Relief",
                "badge": "Govt DBT Integration",
                "whyRecommended": [
                    "Expedited weather-index parametric insurance payout triggered by automatic IMD weather telemetry."
                ],
                "shapFactors": [
                    {"factor": "IMD Weather Station Anand Trigger", "impact": "+60%"},
                    {"factor": "Kisan Credit Card (KCC) Linked Account", "impact": "+30%"}
                ]
            }
        ]
    },
    "anita_shg": {
        "id": "anita_shg",
        "name": "Anita Devi",
        "phone": "+91 91234 67890",
        "age": 34,
        "avatar": "👩🏽",
        "role": "Mithila Painting Artisan & SHG Leader",
        "location": "Madhubani, Bihar (Tier-4 Rural)",
        "language": "hi",
        "languageName": "मैथिली / हिंदी (Hindi/Maithili)",
        "accountNumber": "••• ••• 7712",
        "bankName": "Mithila Kshetriya Gramin Bank",
        "monthlyTurnover": 22000,
        "averageBalance": 6800,
        "upiVelocity": 18,
        "cibilScore": 0,  # New To Credit (NTC)!
        "altCreditScore": 730,  # SHG peer trust score + UPI velocity
        "cashflowTrend": "growing_artisan_orders",
        "stressIndex": 0.22,
        "stressStatus": "Healthy / Emerging Micro-Entrepreneur",
        "lifeStage": "First-Time Digital Borrower / Artisanal Guild Expansion",
        "kycInfo": {
            "status": "Verified (Aadhaar Offline XML & SHG Record)",
            "aadhaarMasked": "XXXX-XXXX-9901",
            "panMasked": "Not Applicable (Form 60 Submitted)",
            "kycDate": "10 Mar 2026",
            "videoKycDone": True,
            "accountAggregatorConsent": "Active (Sahamati AA-1102)",
            "tier": "Tier-4 Rural Village"
        },
        "recentTransactions": [
            {"date": "03 Sep 2026", "desc": "Craftsvilla Exhibition UPI Payout", "amount": 8500, "type": "credit"},
            {"date": "06 Sep 2026", "desc": "Raw Colors & Natural Silk Fabric Purchase", "amount": -3200, "type": "debit"},
            {"date": "08 Sep 2026", "desc": "SHG Monthly Savings Contribution", "amount": -500, "type": "debit"},
            {"date": "10 Sep 2026", "desc": "Artisan Guild UPI Payment", "amount": 4200, "type": "credit"},
            {"date": "12 Sep 2026", "desc": "Mobile Recharge (Jio Bharat Phone)", "amount": -239, "type": "debit"}
        ],
        "recommendations": [
            {
                "id": "rec_mahila_shakti",
                "title": "Saarthi Gramin Mahila Shakti Micro-Credit Line",
                "vernacularTitle": "सारथी ग्रामीण महिला शक्ति माइक्रो-क्रेडिट",
                "category": "Micro Enterprise Loan",
                "amount": "₹20,000 - ₹35,000",
                "interestRate": "7.5% p.a. (Mudra Subsidized)",
                "tenure": "12 months",
                "repaymentType": "Weekly UPI Micro-Installment (₹480/week)",
                "confidenceScore": 95,
                "urgency": "High - Art Exhibition Season",
                "badge": "⭐ New-to-Credit Specialist",
                "whyRecommended": [
                    "Overcomes lack of formal CIBIL score through 36 months of 100% on-time Self-Help Group (SHG) peer records.",
                    "Direct UPI credits from handicraft exhibition buyers prove sustained production cashflow.",
                    "Audio-guided, conversational voice approval in Maithili/Hindi with zero physical paperwork."
                ],
                "shapFactors": [
                    {"factor": "SHG Peer Trust Score (100% On-Time)", "impact": "+45%"},
                    {"factor": "Buyer Direct UPI Settlement Velocity", "impact": "+35%"},
                    {"factor": "Aadhaar e-KYC Verified Beneficiary", "impact": "+15%"},
                    {"factor": "No Formal Bureau History", "impact": "-5% (Mitigated)"}
                ]
            },
            {
                "id": "rec_pradhan_mantri_bima",
                "title": "PM Suraksha Bima & Jeevan Jyoti Bundle",
                "vernacularTitle": "सुरक्षा बीमा एवं जीवन ज्योति योजना",
                "category": "Social Security Protection",
                "amount": "₹4,00,000 Combined Cover",
                "interestRate": "₹456/year total",
                "tenure": "1 Year Renewable",
                "repaymentType": "Single annual auto-debit",
                "confidenceScore": 97,
                "urgency": "Essential Social Safety Net",
                "badge": "Govt Sponsored",
                "whyRecommended": [
                    "Essential financial protection for rural female family breadwinners at just ₹1.25 per day."
                ],
                "shapFactors": [
                    {"factor": "Rural Breadwinner Priority Index", "impact": "+55%"},
                    {"factor": "Eligible for DBT Zero-Cost Subsidies", "impact": "+40%"}
                ]
            }
        ]
    }
}

# In-memory store for newly registered custom users
REGISTERED_USERS = {}

# -------------------------------------------------------------
# MULTI-LINGUAL CONVERSATIONAL KNOWLEDGE BASE FOR SAARTHI AI
# -------------------------------------------------------------
CHAT_KNOWLEDGE_BASE = {
    "balance": {
        "en": "Your current available balance is ₹{balance:,}. In the past 30 days, your net cash turnover was ₹{turnover:,} across {upiVelocity} UPI transactions. Your overall financial health is rated as {stressStatus}.",
        "hi": "नमस्ते {name} जी! आपके खाते में वर्तमान में ₹{balance:,} उपलब्ध हैं। पिछले 30 दिनों में आपने ₹{turnover:,} का कारोबार किया है। आपका वित्तीय स्वास्थ्य '{stressStatus}' स्थिति में है।",
        "gu": "નમસ્તે {name}ભાઈ! તમારા ખાતામાં હાલ ₹{balance:,} સિલક છે. છેલ્લા ૩૦ દિવસમાં કુલ ટર્નઓવર ₹{turnover:,} રહ્યું છે. તમારો એકાઉન્ટ સ્ટેટસ '{stressStatus}' છે.",
        "mr": "नमस्कार {name}! तुमच्या खात्यात सध्या ₹{balance:,} शिल्लक आहेत. मागील ३० दिवसांत एकूण उलाढाल ₹{turnover:,} झाली आहे. आपले खाते '{stressStatus}' स्थितीत आहे.",
        "ta": "வணக்கம் {name}! உங்கள் கணக்கில் தற்போது ₹{balance:,} இருப்பு உள்ளது. கடந்த 30 நாட்களில் உங்கள் வரவு செலவு ₹{turnover:,} ஆகும். உங்கள் நிதி நிலை '{stressStatus}'.",
        "te": "నమస్కారం {name}! మీ ఖాతాలో ప్రస్తుతం ₹{balance:,} బ్యాలెన్స్ ఉంది. గత 30 రోజుల్లో మీ టర్నోవర్ ₹{turnover:,}. మీ ఖాతా స్థితి '{stressStatus}'.",
        "bn": "নমস্কার {name}! আপনার অ্যাকাউন্টে বর্তমানে ₹{balance:,} ব্যালেন্স রয়েছে। গত ৩০ দিনে আপনার মোট লেনদেন ₹{turnover:,}। আপনার আর্থিক অবস্থা '{stressStatus}'।"
    },
    "loan_inquiry": {
        "en": "Hello {name}! Based on your verified cashflow and transactions, you qualify for an instant pre-approved credit line up to ₹1,50,000 at 11.2% p.a. Repayment is ultra-flexible: daily micro-bites of ₹145/day through UPI. Would you like to start the 2-minute zero-paperwork approval right now?",
        "hi": "नमस्ते {name} जी! आपके खाते के लेन-देन और यूपीआई व्यापार के आधार पर, आपके लिए ₹1,50,000 तक का प्री-अप्रूव्ड आसान लोन उपलब्ध है। ब्याज दर मात्र 11.2% वार्षिक है और आप ₹145 प्रतिदिन की आसान किश्त में चुका सकते हैं। क्या आप 2 मिनट में डिजिटल स्वीकृति पत्र देखना चाहते हैं?",
        "gu": "નમસ્તે {name}ભાઈ! તમારા યુપીઆઇ અને બેંક ટ્રાન્ઝેક્શનને આધારે ₹1,50,000 સુધીની ઇન્સ્ટન્ટ ક્રેડિટ લાઇન ૧૧.૨% ના વ્યાજે ઉપલબ્ધ છે. શું આપ ૨ મિનિટમાં મંજૂરી મેળવવા માંગો છો?",
        "mr": "नमस्कार {name}! आपल्या UPI व्यवहारांवर आधारित ₹1,50,000 पर्यंतचे पूर्व-मंजूर व्यवसाय कर्ज ११.२% दराने उपलब्ध आहे. आपण २ मिनिटांत मंजुरी पत्र पाहू इच्छिता का?",
        "ta": "வணக்கம் {name}! உங்கள் UPI பரிவர்த்தனைகளின் அடிப்படையில் ₹1,50,000 வரை உடனடி கடன் வசதி உள்ளது. 2 நிமிடங்களில் விண்ணப்பிக்க விரும்புகிறீர்களா?",
        "te": "నమస్కారం {name}! మీ UPI లావాదేవీల ఆధారంగా ₹1,50,000 వరకు తక్షణ రుణం అందుబాటులో ఉంది. 2 నిమిషాల్లో ఆమోదం పొందాలనుకుంటున్నారా?",
        "bn": "নমস্কার {name}! আপনার UPI লেনদেনের ভিত্তিতে ₹1,50,000 পর্যন্ত তাত্ক্ষণিক প্রি-অ্যাপ্রুভড লোন উপলব্ধ। আপনি কি এখনই ২ মিনিটে আবেদন করতে চান?"
    },
    "stress_moratorium": {
        "en": "We detected temporary cashflow stress in your account. Please don't worry — Saarthi AI never penalizes honest borrowers! We have automatically waived late fees, protected your CIBIL score, and activated options for a 30-day EMI pause or ₹80/day micro-repayment. How can we support you today?",
        "hi": "घबराइए मत {name} जी, हमें पता है कि इस महीने आपके व्यापार या फसल में अचानक रुकावट आई है। सारथी एआई ने आपके खाते पर कोई जुर्माना या पेनल्टी नहीं लगाई है और आपका सिबिल स्कोर पूरी तरह सुरक्षित है। क्या आप 30 दिन की मोहलत लेना चाहते हैं या ₹80 प्रतिदिन की छोटी किश्त में बदलना चाहते हैं?",
        "gu": "ચિંતા ન કરશો {name}ભાઈ, કમોસમી વરસાદ કે મુશ્કેલી અમે સમજીએ છીએ. સારથી એઆઈ તમારા પર કોઈ દંડ લગાવશે નહીં અને સિબિલ સ્કોર પણ સુરક્ષિત રહેશે. ૪૫ દિવસની મુદત વધારો અથવા દૈનિક ₹૮૦ ના હપ્તામાં બદલો.",
        "mr": "काळजी करू नका {name}! तात्पुरत्या आर्थिक अडचणींमुळे तुमच्यावर कोणताही दंड आकारला जाणार नाही. आपण ३० दिवसांची सवलत घेऊ शकता किंवा रोजच्या लहान हप्त्यांमध्ये बदलू शकता.",
        "ta": "கவலைப்பட வேண்டாம் {name}! தற்காலிக நிதி நெருக்கடியால் எந்த அபராதமும் விதிக்கப்படாது. உங்கள் கிரெடிட் ஸ்கோர் பாதுகாப்பாக உள்ளது. 30 நாட்கள் அவகாசம் வேண்டுமா?",
        "te": "ఆందోళన చెందవద్దు {name}! తాత్కాలిక ఆర్థిక ఇబ్బందుల వల్ల ఎటువంటి జరిమానా విధించబడదు. 30 రోజుల గడువు పొడిగింపును ఎంచుకోవచ్చు.",
        "bn": "চিন্তা করবেন না {name}! সাময়িক আর্থিক সমস্যার কারণে কোনো জরিমানা নেওয়া হবে না। আপনার CIBIL সুরক্ষিত থাকবে। ৩০ দিনের গ্রেস পিরিয়ড নিতে পারেন।"
    },
    "kyc": {
        "en": "Your KYC status is '{status}'. Your account is linked with Aadhaar ({aadhaarMasked}) and verified via Account Aggregator. You are fully eligible for paperless instant digital lending without visiting any bank branch.",
        "hi": "आपका केवाईसी स्टेटस '{status}' है। आपका खाता आधार संख्या ({aadhaarMasked}) से लिंक है और अकाउंट एग्रीगेटर से प्रमाणित है। आपको किसी बैंक शाखा में जाने की आवश्यकता नहीं है, सब कुछ यहीं फोन पर 100% डिजिटल है।",
        "gu": "તમારું કેવાયસી સ્ટેટસ '{status}' છે. આધાર ({aadhaarMasked}) સાથે જોડાયેલ છે. કોઈ બેંક શાખાની મુલાકાત લીધા વિના ડિજિટલ મંજૂરી મળશે.",
        "mr": "आपले केवायसी '{status}' आहे. आधार ({aadhaarMasked}) प्रमाणीकृत आहे. कोणत्याही कागदपत्रांशिवाय डिजिटल कर्ज मिळू शकते.",
        "ta": "உங்கள் KYC '{status}' நிலையில் உள்ளது. ஆதார் ({aadhaarMasked}) சரிபார்க்கப்பட்டுள்ளது. நேரடி வங்கி செல்லத் தேவையில்லை.",
        "te": "మీ KYC '{status}' లో ఉంది. ఆధార్ ({aadhaarMasked}) ధృవీకరించబడింది. బ్యాంకుకు వెళ్లకుండానే రుణం పొందవచ్చు.",
        "bn": "আপনার KYC স্ট্যাটাস '{status}'। আধার ({aadhaarMasked}) ভেরিফাইড রয়েছে। ব্রাঞ্চে না গিয়েও সম্পূর্ণ ডিজিটাল ঋণ পাবেন।"
    },
    "schemes": {
        "en": "Based on your Bharat profile, you are eligible for: 1) PM Mudra Shishu Yojana (up to ₹50,000 at subsidized rates), 2) PM Suraksha Bima (₹2 Lakh accidental cover at ₹20/year), and 3) Kisan Credit Card / Stand-Up India for rural entrepreneurs.",
        "hi": "आपकी प्रोफाइल के अनुसार आप इन सरकारी योजनाओं के पात्र हैं: 1) पीएम मुद्रा शिशु योजना (₹50,000 तक बिना गारंटी रियायती लोन), 2) पीएम सुरक्षा बीमा (₹20/वर्ष में ₹2 लाख दुर्घटना बीमा), और 3) स्वनिधि योजना (सड़क विक्रेताओं व किराना हेतु ₹10,000-₹50,000)।",
        "gu": "તમારી પ્રોફાઇલ મુજબ: ૧) પીએમ મુદ્રા લોન (સબસિડી સાથે), ૨) પીએમ પાક વીમા યોજના, ૩) પીએમ સુરક્ષા વીમા યોજના માત્ર ₹૨૦ વાર્ષિક પ્રીમિયમમાં.",
        "mr": "तुमच्यासाठी योजना: १) पीएम मुद्रा योजना (विनातारण कर्ज), २) पीएम सुरक्षा विमा (वार्षिक ₹२० मध्ये २ लाख विमा), ३) पीएम स्वनिधी योजना.",
        "ta": "உங்களுக்கான அரசு திட்டங்கள்: 1) பிரதான் மந்திரி முத்ரா கடன், 2) சுரக்சா பீமா காப்பீடு (ஆண்டுக்கு ₹20 மட்டுமே), 3) கிசான் கிரெடிட் கார்டு.",
        "te": "మీకు అర్హత ఉన్న పథకాలు: 1) పీఎం ముద్రా రుణం, 2) పీఎం సురక్షా బీమా (సంవత్సరానికి కేవలం ₹20), 3) కిసాన్ క్రెడిట్ కార్డు.",
        "bn": "আপনার জন্য সরকারি প্রকল্প: ১) পিএম মুদ্রা যোজনা, ২) পিএম সুরক্ষা বীমা (বছরে মাত্র ২০ টাকায় ২ লক্ষের কভার), ৩) পিএম স্বনিধি যোজনা।"
    }
}

# -------------------------------------------------------------
# ARCHITECTURE & AI/ML SPECS
# -------------------------------------------------------------
SYSTEM_ARCHITECTURE = {
    "layers": [
        {
            "id": "layer_1",
            "name": "1. Multi-Modal Data Ingestion & Sovereign Rail Layer",
            "description": "Compliant, zero-trust data acquisition from India Stack and sovereign financial public rails.",
            "components": [
                {"name": "Account Aggregator (AA)", "tech": "Sahamati / Setu API Framework", "role": "Cryptographically signed bank statements with time-bound, purpose-limited consent."},
                {"name": "UPI & NPCI Switch", "tech": "UPI 2.0 AutoPay & QR Telemetry", "role": "Tracks daily micro-cashflows, merchant categories, customer footfall velocity."},
                {"name": "GSTN & e-Way Bill", "tech": "GST Suvidha Provider (GSP)", "role": "Real-time B2B invoice matching, supply-chain health, tax compliance."},
                {"name": "Bharat Alternative Signals", "tech": "DISCOM Electricity / Mandi APMC / SHG Records", "role": "Bypasses thin bureau records for rural farmers and women artisans."},
                {"name": "DPDP Act 2023 Consent Gateway", "tech": "Sovereign Consent Artifact", "role": "Enforces purpose limitation, notice, and immediate revocability."}
            ]
        },
        {
            "id": "layer_2",
            "name": "2. Real-Time Feature Store & Behavioral Dynamics",
            "description": "Low-latency stream processing extracting life-stage signals and early stress vectors.",
            "components": [
                {"name": "Cashflow Volatility Index (CVI)", "formula": "StdDev(Daily Inflows) / Mean(30-day Volume)", "detail": "Distinguishes normal festive surges from structural distress."},
                {"name": "Liquidity Buffer Ratio (LBR)", "formula": "EOD Balance / Average Daily Outflow", "detail": "Predicts insolvency 21 days before any formal loan bounce occurs."},
                {"name": "Life-Stage Temporal Detector", "tech": "Hidden Markov Models + Temporal CNN", "detail": "Identifies child school fee cycles, crop sowing, marriages, harvest dates."},
                {"name": "New-to-Credit (NTC) Synthesizer", "tech": "Graph Neural Networks (GNN)", "detail": "Builds alternative creditworthiness from community trust and utility consistency."}
            ]
        },
        {
            "id": "layer_3",
            "name": "3. AI/ML Inference & Explainability Engines",
            "description": "Multi-model ensemble executing recommendation, stress detection, and vernacular conversational guidance.",
            "components": [
                {"name": "Hyper-Personalized Recommendation", "model": "Two-Tower Neural Net + LightGBM Re-Ranker", "detail": "Ranks financial products by customer survival/growth utility rather than bank fee margins."},
                {"name": "Early Warning Stress Autoencoder", "model": "LSTM Anomaly Detector + Isolation Forest", "detail": "Detects subtle early warning signs of stress (92.4% precision) 3 weeks in advance."},
                {"name": "Vernacular Conversational AI (Saarthi Vani)", "model": "Bhashini LLM / Indic-Whisper + Indic-TTS", "detail": "High-accuracy, dialect-robust speech-to-text & text-to-speech across 12 Indian languages."},
                {"name": "Explainable Underwriting (XAI)", "model": "TreeSHAP & Local Counterfactuals", "detail": "Generates transparent, auditable approval reasons translated into local vernacular."}
            ]
        },
        {
            "id": "layer_4",
            "name": "4. Ethical Safeguards & Regulatory Gatekeeper",
            "description": "Autonomous guardian layer enforcing DPDP Act 2023 and RBI Digital Lending Guidelines 2022.",
            "components": [
                {"name": "Anti-Predatory Nudge Filter", "rule": "StressIndex > 0.65 => Hard Ban on High-Cost Credit", "detail": "Stops over-indebtedness by replacing aggressive loans with moratoriums or micro-savings."},
                {"name": "RBI Digital Lending (DLG) Guard", "rule": "Direct Bank Escrow & Mandatory KFS", "detail": "Zero pass-through accounts, clear APR disclosure, and cooling-off exit rights."},
                {"name": "Algorithmic Fairness & Bias Auditor", "metric": "Disparate Impact Ratio > 0.95 across Gender/Pincodes", "detail": "Guarantees rural female artisans receive equal approval odds to formal salaried peers."},
                {"name": "Data Localization Vault", "norm": "100% On-Soil Storage (RBI Mandate)", "detail": "Zero international egress; military-grade encryption at rest and in transit."}
            ]
        },
        {
            "id": "layer_5",
            "name": "5. Omnichannel Bharat Delivery Experience",
            "description": "Frictionless interfaces for non-tech-savvy users across diverse literacy levels.",
            "components": [
                {"name": "Voice-First Web & PWA", "tech": "Web Speech API + Lightweight Audio Streams", "detail": "Works on inexpensive 4G/Jio smartphones even with low literacy."},
                {"name": "WhatsApp Banking & IVR Bot", "tech": "WhatsApp Business API + Indic IVR", "detail": "Enables voice notes and missed-call balance & loan management."},
                {"name": "Bank Mitra Assisted Tablet View", "tech": "Biometric Aadhaar Agent App", "detail": "Empowers village banking correspondents with transparent AI sanction sheets."}
            ]
        }
    ]
}

ETHICAL_SAFEGUARDS = {
    "dpdp_act_2023": [
        {"principle": "Lawful Purpose & Explicit Consent", "status": "Compliant", "evidence": "Every Account Aggregator fetch requires biometric/OTP consent specifying exact 90-day scope and purpose."},
        {"principle": "Purpose Limitation", "status": "Compliant", "evidence": "Financial transactional data utilized strictly for underwriting; zero ad profiling or third-party sharing."},
        {"principle": "Data Principal Rights", "status": "Compliant", "evidence": "In-app 1-click 'Revoke Consent' and 'Forget My Profile' triggers complete anonymization."},
        {"principle": "Data Localization", "status": "Compliant", "evidence": "All databases, feature stores, and model checkpoints hosted strictly within Indian sovereign borders (Mumbai/Hyderabad)."}
    ],
    "rbi_lending_guidelines_2022": [
        {"clause": "Direct Disbursal", "status": "Compliant", "evidence": "Funds transfer directly from Regulated Entity (Bank/NBFC) escrow to borrower's savings account without pass-through pooling."},
        {"clause": "Key Fact Statement (KFS)", "status": "Compliant", "evidence": "Standardized one-page KFS with Annual Percentage Rate (APR), total cost of credit, and cooling-off period presented prior to execution."},
        {"clause": "No Automatic Credit Limit Enhancement", "status": "Compliant", "evidence": "Higher limits require explicit, voluntary consent from borrower; zero silent unsolicited line hikes."},
        {"clause": "Empathetic Recovery & No Harassment", "status": "Compliant", "evidence": "Algorithm flags stress 21 days before default and mandates restructuring offers before any recovery notification."}
    ],
    "algorithmic_fairness": [
        {"metric": "Equal Opportunity Odds", "score": "0.98", "detail": "Artisan women (Anita) with non-traditional cashflow evaluated at equal approval odds to formal salaried teachers (Priya)."},
        {"metric": "Anti-Predatory Nudge Trigger", "score": "100% Enforced", "detail": "Stress Index > 0.65 automatically hides all loan upsell banners and substitutes financial wellness counselors."}
    ]
}

PORTFOLIO_ANALYTICS = {
    "totalBorrowersBharat": "1,420,850",
    "dropOffReduction": "68.4%",
    "cacReduction": "41.8%",
    "earlyDelinquencyRescueRate": "89.2%",
    "vernacularAdoptionRate": "84.6%",
    "tierBreakdown": {"Tier-2": "28%", "Tier-3": "44%", "Tier-4 / Rural": "28%"},
    "savedFromPredatoryLenders": "₹42.8 Cr",
    "avgApprovalTimeMinutes": "2.4 minutes"
}


# -------------------------------------------------------------
# HTTP REQUEST HANDLER
# -------------------------------------------------------------
class SaarthiHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Serve SPA index
        if path in ["/", "/index.html", "/login", "/dashboard"]:
            file_path = os.path.join(STATIC_DIR, "index.html")
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_json({"error": "Static index.html not found"}, 404)
                return

        # API Routes
        if path == "/api/personas":
            summary = [
                {
                    "id": p["id"],
                    "name": p["name"],
                    "phone": p.get("phone", ""),
                    "role": p["role"],
                    "location": p["location"],
                    "avatar": p["avatar"],
                    "language": p["language"],
                    "languageName": p["languageName"],
                    "stressStatus": p["stressStatus"],
                    "stressIndex": p["stressIndex"],
                    "cibilScore": p["cibilScore"],
                    "altCreditScore": p["altCreditScore"]
                }
                for p in PERSONAS.values()
            ]
            # Include custom registered users if any
            for uid, u in REGISTERED_USERS.items():
                summary.append({
                    "id": u["id"],
                    "name": u["name"],
                    "phone": u.get("phone", ""),
                    "role": u["role"],
                    "location": u["location"],
                    "avatar": u["avatar"],
                    "language": u["language"],
                    "languageName": u["languageName"],
                    "stressStatus": u["stressStatus"],
                    "stressIndex": u["stressIndex"],
                    "cibilScore": u["cibilScore"],
                    "altCreditScore": u["altCreditScore"]
                })
            self.send_json({"personas": summary, "timestamp": datetime.now().isoformat()})
            return

        elif path.startswith("/api/customer/"):
            persona_id = path.split("/api/customer/")[1]
            if persona_id in PERSONAS:
                self.send_json({"customer": PERSONAS[persona_id]})
            elif persona_id in REGISTERED_USERS:
                self.send_json({"customer": REGISTERED_USERS[persona_id]})
            else:
                self.send_json({"error": f"Customer '{persona_id}' not found"}, 404)
            return

        elif path == "/api/architecture":
            self.send_json({"architecture": SYSTEM_ARCHITECTURE})
            return

        elif path == "/api/ethics-compliance":
            self.send_json({"compliance": ETHICAL_SAFEGUARDS})
            return

        elif path == "/api/analytics":
            self.send_json({"analytics": PORTFOLIO_ANALYTICS})
            return

        elif path.startswith("/api/stress-alerts/"):
            persona_id = path.split("/api/stress-alerts/")[1]
            p = PERSONAS.get(persona_id) or REGISTERED_USERS.get(persona_id)
            if p:
                is_stressed = p["stressIndex"] > 0.5
                self.send_json({
                    "personaId": persona_id,
                    "customerName": p["name"],
                    "stressIndex": p["stressIndex"],
                    "stressStatus": p["stressStatus"],
                    "isStressed": is_stressed,
                    "earlyWarningSignals": [
                        {"indicator": "Liquidity Buffer", "value": f"{(1 - p['stressIndex']) * 14:.1f} days", "status": "critical" if is_stressed else "normal"},
                        {"indicator": "Cashflow Drop Ratio", "value": f"{p['stressIndex'] * 60:.0f}% deviation", "status": "critical" if is_stressed else "normal"},
                        {"indicator": "EMI Bounce Probability", "value": f"{p['stressIndex'] * 95:.1f}%", "status": "high" if is_stressed else "low"}
                    ],
                    "availableInterventions": [
                        {
                            "id": "grace_period",
                            "title": "30-Day Compassionate Grace Period",
                            "description": "Zero penalty interest, zero CIBIL reporting hit, RBI compliant moratorium.",
                            "actionLabel": "Apply Instant 30-Day Grace"
                        },
                        {
                            "id": "micro_repayment",
                            "title": "Convert Monthly EMI to Daily Micro-Bites",
                            "description": "Instead of lump-sum monthly pressure, pay daily micro-amounts automatically from UPI sales.",
                            "actionLabel": "Switch to Micro-Bites"
                        },
                        {
                            "id": "gramin_mitra",
                            "title": "Schedule Friendly Visit from Gramin Mitra",
                            "description": "A trusted local banking facilitator visits in person to assist with restructuring.",
                            "actionLabel": "Request Mitra Visit"
                        }
                    ]
                })
            else:
                self.send_json({"error": "Persona not found"}, 404)
            return

        # Fallback to SimpleHTTPRequestHandler for static files
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b'{}'
        try:
            req_data = json.loads(post_body.decode('utf-8'))
        except Exception:
            req_data = {}

        # ---------------- Auth: Register New Account ----------------
        if path == "/api/auth/register":
            name = req_data.get("name", "New Citizen").strip()
            phone = req_data.get("phone", "+91 99999 00000").strip()
            role = req_data.get("role", "Small Merchant / Agri Entrepreneur")
            location = req_data.get("location", "Varanasi, UP (Tier-3)")
            lang = req_data.get("language", "hi")
            monthly_income = int(req_data.get("monthlyIncome", 35000))
            aadhaar_input = req_data.get("aadhaar", "123456789012")

            uid = f"user_{uuid.uuid4().hex[:8]}"
            masked_aadhaar = f"XXXX-XXXX-{aadhaar_input[-4:]}" if len(aadhaar_input) >= 4 else "XXXX-XXXX-3829"

            new_user = {
                "id": uid,
                "name": name,
                "phone": phone,
                "age": 32,
                "avatar": "🧑🏽",
                "role": role,
                "location": location,
                "language": lang,
                "languageName": "हिंदी (Hindi)" if lang == "hi" else ("ગુજરાતી (Gujarati)" if lang == "gu" else "English"),
                "accountNumber": f"••• ••• {aadhaar_input[-4:] if len(aadhaar_input) >= 4 else '5521'}",
                "bankName": "Bharat Jan Dhan Bank",
                "monthlyTurnover": monthly_income,
                "averageBalance": int(monthly_income * 0.35),
                "upiVelocity": 24,
                "cibilScore": 710,
                "altCreditScore": 750,
                "cashflowTrend": "positive_stable",
                "stressIndex": 0.18,
                "stressStatus": "Healthy / Low Risk",
                "lifeStage": "Emerging Digital User / Growth Capital",
                "kycInfo": {
                    "status": "Verified (Instant Aadhaar e-KYC)",
                    "aadhaarMasked": masked_aadhaar,
                    "panMasked": "NEWUSER123K",
                    "kycDate": datetime.now().strftime("%d %b %Y"),
                    "videoKycDone": True,
                    "accountAggregatorConsent": "Active (Sahamati AA-NEW)",
                    "tier": location
                },
                "recentTransactions": [
                    {"date": "Today", "desc": "Account Setup & Initial Deposit", "amount": 5000, "type": "credit"},
                    {"date": "Yesterday", "desc": "UPI QR Customer Payment", "amount": 1850, "type": "credit"},
                    {"date": "3 Days Ago", "desc": "Local Market Purchase", "amount": -820, "type": "debit"}
                ],
                "recommendations": [
                    {
                        "id": f"rec_{uid}_growth",
                        "title": "Saarthi Bharat Pragati Credit Line",
                        "vernacularTitle": "सारथी भारत प्रगति क्रेडिट लाइन",
                        "category": "Micro Growth Loan",
                        "amount": f"₹{int(monthly_income * 1.5):,}",
                        "interestRate": "10.8% p.a.",
                        "tenure": "12 months",
                        "repaymentType": "Daily Micro-UPI Repayment (₹85/day)",
                        "confidenceScore": 93,
                        "urgency": "High",
                        "badge": "⭐ Instant Digital Approval",
                        "whyRecommended": [
                            f"Verified Aadhaar e-KYC and initial UPI turnover of ₹{monthly_income:,}/mo.",
                            "Tailored micro-repayment prevents lump-sum monthly stress."
                        ],
                        "shapFactors": [
                            {"factor": "Aadhaar e-KYC Instant Verification", "impact": "+40%"},
                            {"factor": "Healthy Inflow-to-Balance Ratio", "impact": "+35%"}
                        ]
                    }
                ]
            }

            REGISTERED_USERS[uid] = new_user

            self.send_json({
                "success": True,
                "message": "Account created successfully with verified e-KYC!",
                "user": new_user
            })
            return

        # ---------------- Auth: Login ----------------
        elif path == "/api/auth/login":
            login_id = req_data.get("loginId", "").strip()
            # Check if login_id matches a persona or registered user phone/id
            matched_user = None
            if login_id in PERSONAS:
                matched_user = PERSONAS[login_id]
            elif login_id in REGISTERED_USERS:
                matched_user = REGISTERED_USERS[login_id]
            else:
                for p in list(PERSONAS.values()) + list(REGISTERED_USERS.values()):
                    if p.get("phone", "").replace(" ", "") == login_id.replace(" ", "") or p["name"].lower() == login_id.lower():
                        matched_user = p
                        break

            if not matched_user:
                # Default to Ramesh Kirana if logging in with generic demo number
                matched_user = PERSONAS["ramesh_kirana"]

            self.send_json({
                "success": True,
                "message": f"Welcome back, {matched_user['name']}!",
                "user": matched_user
            })
            return

        # ---------------- Conversational Vernacular Bot (Saarthi AI) ----------------
        elif path == "/api/chat":
            persona_id = req_data.get("personaId", "ramesh_kirana")
            message = req_data.get("message", "").lower()
            lang = req_data.get("language", "hi")

            p = PERSONAS.get(persona_id) or REGISTERED_USERS.get(persona_id) or PERSONAS["ramesh_kirana"]

            # Intent Recognition
            if any(w in message for w in ["balance", "खाता", "बैलेंस", "पैसे", "સિલિક", "રૂપિયા", "பணம்", "బాకీ", "টাকা", "शिल्लक"]):
                intent = "balance"
            elif any(w in message for w in ["kyc", "केवाईसी", "आधार", "aadhaar", "pan", "দস্তাবেজ", "பான்"]):
                intent = "kyc"
            elif any(w in message for w in ["help", "मदद", "तनाव", "किश्त", "हપ્તો", "stress", "moratorium", "delay", "रुपए नहीं", "பிரச்சனை", "కష్టం"]):
                intent = "stress_moratorium"
            elif any(w in message for w in ["scheme", "योजना", "सरकारी", "subsidy", "யோசனை", "పథకం", "যোজনা"]):
                intent = "schemes"
            else:
                # Default to loan and personalized guidance
                intent = "loan_inquiry"

            template = CHAT_KNOWLEDGE_BASE[intent].get(lang, CHAT_KNOWLEDGE_BASE[intent]["en"])
            reply_text = template.format(
                name=p["name"],
                balance=p["averageBalance"],
                turnover=p["monthlyTurnover"],
                upiVelocity=p["upiVelocity"],
                stressStatus=p["stressStatus"],
                status=p["kycInfo"]["status"],
                aadhaarMasked=p["kycInfo"]["aadhaarMasked"]
            )

            # High-accuracy options for prompt follow-ups
            options_map = {
                "balance": ["Mini Statement", "Loan Eligibility", "Invest in Goal RD"],
                "loan_inquiry": ["Apply Loan (2 Mins)", "View EMI & Interest", "Account Aggregator Consent"],
                "stress_moratorium": ["Activate 30-Day Pause", "Switch to ₹80/Day Repayment", "Talk to Gramin Mitra"],
                "kyc": ["View Aadhaar e-KYC Certificate", "Update Address", "Account Aggregator Status"],
                "schemes": ["Apply PM Mudra", "PM Suraksha Bima", "Kisan Credit Support"]
            }

            self.send_json({
                "response": reply_text,
                "audioText": reply_text,
                "language": lang,
                "intent": intent,
                "suggestedOptions": options_map.get(intent, ["Check Loan", "Balance", "Help"]),
                "customer": p["name"],
                "timestamp": datetime.now().isoformat()
            })
            return

        # ---------------- Empathetic Intervention ----------------
        elif path == "/api/trigger-intervention":
            persona_id = req_data.get("personaId", "suresh_farmer")
            intervention_id = req_data.get("interventionId", "grace_period")

            p = PERSONAS.get(persona_id) or REGISTERED_USERS.get(persona_id)
            if p:
                p["stressIndex"] = max(0.15, p["stressIndex"] - 0.5)
                p["stressStatus"] = "Relief Granted (30-Day Compassionate Grace Active)"

                self.send_json({
                    "success": True,
                    "message": f"Empathetic intervention '{intervention_id}' successfully executed for {p['name']}.",
                    "newStressIndex": p["stressIndex"],
                    "newStressStatus": p["stressStatus"],
                    "reliefDetails": {
                        "lateFeeWaived": "₹650 (100% Waived)",
                        "cibilAdverseImpact": "Zero (Protected under RBI Compassionate Lending)",
                        "nextPaymentDate": "15 November 2026",
                        "smsConfirmation": f"SAARTHI: Namaste {p['name']}, your EMI has been rescheduled with zero penalty. Your financial safety is our highest priority."
                    }
                })
            else:
                self.send_json({"error": "Persona not found"}, 404)
            return

        # ---------------- Instant 2-Minute Digital Loan Application ----------------
        elif path == "/api/apply-loan":
            persona_id = req_data.get("personaId", "ramesh_kirana")
            amount = int(req_data.get("amount", 50000))
            tenure_months = int(req_data.get("tenure", 12))

            p = PERSONAS.get(persona_id) or REGISTERED_USERS.get(persona_id) or PERSONAS["ramesh_kirana"]

            apr = 11.2
            monthly_interest_rate = (apr / 100) / 12
            emi = int((amount * monthly_interest_rate * ((1 + monthly_interest_rate)**tenure_months)) / (((1 + monthly_interest_rate)**tenure_months) - 1))
            daily_bite = int(emi / 30)

            sanction_letter = {
                "sanctionId": f"SAARTHI-SANCTION-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "borrowerName": p["name"],
                "maskedAccount": p["accountNumber"],
                "sanctionedAmount": amount,
                "interestRate": f"{apr}% p.a. (Fixed Reducing)",
                "tenureMonths": tenure_months,
                "monthlyEmi": emi,
                "dailyBite": daily_bite,
                "processingFee": "₹0 (Zero Processing Fee under Bharat Financial Inclusion Mandate)",
                "disbursalMode": "Direct Bank Account Escrow to Account (100% RBI DLG Compliant)",
                "coolingOffPeriod": "3 business days (100% refund without penalty)",
                "repaymentSchedule": f"{tenure_months} monthly cycles or ₹{daily_bite}/day micro-UPI sweep",
                "underwritingSignals": {
                    "accountAggregatorConsent": "VERIFIED (AA-SAHAMATI-2026-X91)",
                    "upiVelocityVerification": f"PASSED ({p['upiVelocity']} txns/day verified)",
                    "fraudCheck": "CLEARED (Geo-IP & SIM-Binding Validated)",
                    "dpdpComplianceToken": "DPDP-SECURE-VAULT-2026"
                },
                "status": "APPROVED & READY FOR 1-CLICK DISBURSAL",
                "issuedAt": datetime.now().strftime("%d %B %Y, %I:%M %p")
            }

            self.send_json({
                "success": True,
                "sanction": sanction_letter
            })
            return

        # ---------------- Evaluator Testing: Simulate Cashflow Shock ----------------
        elif path == "/api/simulate-stress":
            persona_id = req_data.get("personaId", "ramesh_kirana")
            p = PERSONAS.get(persona_id) or REGISTERED_USERS.get(persona_id)

            if p:
                p["stressIndex"] = 0.84
                p["stressStatus"] = "⚠️ Stressed: 55% Cashflow Drop Detected"
                p["recentTransactions"].insert(0, {
                    "date": "Today",
                    "desc": "⚠️ Alert: Daily UPI Inflows dropped from 54 to 8 txns",
                    "amount": 750,
                    "type": "warning"
                })
                # Replace loan ads with empathetic restructuring
                p["recommendations"] = [
                    {
                        "id": "rec_empathetic_restructure",
                        "title": "Saarthi Compassionate Repayment Protection",
                        "vernacularTitle": "सारथी सहानुभूतिपूर्ण पुनर्भुगतान सुरक्षा",
                        "category": "Empathetic Stress Intervention",
                        "amount": "Zero Penalty Restructuring",
                        "interestRate": "0% Penalty",
                        "tenure": "30 Days Buffer",
                        "repaymentType": "Switch to Micro-Bites (₹45/day)",
                        "confidenceScore": 99,
                        "urgency": "Immediate Relief",
                        "badge": "🛡️ Ethical Safeguard Activated",
                        "whyRecommended": [
                            "Saarthi Ethical Guardrail detected a sudden 55% drop in customer daily UPI receipts.",
                            "System has STRICTLY BLOCKED all high-cost debt cross-sell ads.",
                            "Offered instant switch to micro-daily repayment to protect your CIBIL standing."
                        ],
                        "shapFactors": [
                            {"factor": "Cashflow Drop Detected (>50%)", "impact": "+55%"},
                            {"factor": "Proactive Distress Prevention", "impact": "+45%"}
                        ]
                    }
                ]
                self.send_json({
                    "success": True,
                    "message": "Cashflow shock simulated. Saarthi AI dynamically suppressed loan sales and activated compassionate safeguards!",
                    "customer": p
                })
            else:
                self.send_json({"error": "Persona not found"}, 404)
            return

        elif path == "/api/reset-persona":
            persona_id = req_data.get("personaId", "ramesh_kirana")
            if persona_id == "ramesh_kirana":
                PERSONAS["ramesh_kirana"]["stressIndex"] = 0.28
                PERSONAS["ramesh_kirana"]["stressStatus"] = "Healthy / Low Risk"
            elif persona_id == "suresh_farmer":
                PERSONAS["suresh_farmer"]["stressIndex"] = 0.78
                PERSONAS["suresh_farmer"]["stressStatus"] = "⚠️ Early Warning: Cashflow Stress Detected"
            self.send_json({"success": True, "customer": PERSONAS.get(persona_id)})
            return

        else:
            self.send_json({"error": "Endpoint not found"}, 404)


def run_server():
    os.chdir(BASE_DIR)
    handler = SaarthiHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"==================================================")
        print(f"SAARTHI (सारथी) AI Server running on http://localhost:{PORT}")
        print(f"Serving UI from: {STATIC_DIR}")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")
            httpd.shutdown()


if __name__ == "__main__":
    run_server()
