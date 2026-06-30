const diseaseKnowledge = {
  fever: {
    overview:
      "Fever is a higher than normal body temperature, usually caused by infection or inflammation.",
    common_symptoms: ["high temperature", "chills", "body pain", "tiredness"],
    care_guidance: [
      "keep the patient hydrated",
      "use fever medicine only as prescribed",
      "recheck temperature regularly"
    ],
    prevention_tips: ["wash hands often", "avoid close contact during infections"],
    urgent_warning_signs: [
      "fever is very high",
      "breathing is difficult",
      "symptoms last more than 3 days"
    ]
  },
  cough: {
    overview:
      "Cough is a reflex that clears the throat or lungs and can happen with colds, allergy, asthma, or infection.",
    common_symptoms: ["throat irritation", "mucus", "chest discomfort"],
    care_guidance: [
      "stay away from smoke, dust, and strong smells",
      "drink warm fluids if comfortable",
      "take prescribed cough or allergy medicine only as directed"
    ],
    prevention_tips: ["cover coughs", "wash hands often", "avoid known allergens"],
    urgent_warning_signs: [
      "cough lasts more than 2 weeks",
      "blood appears",
      "breathing is difficult"
    ]
  },
  cold: {
    overview: "Common cold is a mild viral infection of the nose and throat.",
    common_symptoms: ["runny nose", "sneezing", "sore throat", "mild cough"],
    care_guidance: [
      "rest and drink enough fluids",
      "use prescribed symptom medicines only as directed",
      "avoid unnecessary antibiotics unless a doctor prescribes them"
    ],
    prevention_tips: ["wash hands often", "avoid sharing cups or towels"],
    urgent_warning_signs: [
      "high fever occurs",
      "symptoms worsen",
      "breathing becomes difficult"
    ]
  },
  headache: {
    overview:
      "Headache is pain in the head or face and may be caused by stress, dehydration, fever, migraine, or other conditions.",
    common_symptoms: ["head pain", "light sensitivity", "nausea"],
    care_guidance: [
      "drink water and eat on time",
      "rest away from bright light and loud noise",
      "take pain medicine only as prescribed"
    ],
    prevention_tips: ["sleep regularly", "manage stress", "avoid known triggers"],
    urgent_warning_signs: [
      "pain is sudden and severe",
      "vision changes",
      "weakness or confusion occurs"
    ]
  },
  diabetes: {
    overview:
      "Diabetes is a long-term condition where blood sugar stays higher than normal.",
    common_symptoms: [
      "frequent urination",
      "increased thirst",
      "tiredness",
      "slow wound healing"
    ],
    care_guidance: [
      "follow the diet and medicine plan from the doctor",
      "check blood sugar as advised",
      "keep regular follow-up visits"
    ],
    prevention_tips: [
      "choose balanced meals",
      "stay physically active as advised",
      "maintain a healthy weight"
    ],
    urgent_warning_signs: [
      "blood sugar is very high or low",
      "vomiting occurs",
      "confusion or fainting occurs"
    ]
  },
  hypertension: {
    overview:
      "Hypertension means high blood pressure, which can increase risk to the heart, brain, and kidneys.",
    common_symptoms: ["often no symptoms", "headache", "dizziness"],
    care_guidance: [
      "take blood pressure medicine at the same time each day",
      "reduce salt if advised",
      "record blood pressure readings for follow-up"
    ],
    prevention_tips: [
      "limit salt",
      "stay active as advised",
      "avoid tobacco and excess alcohol"
    ],
    urgent_warning_signs: [
      "chest pain occurs",
      "severe headache occurs",
      "blood pressure is very high"
    ]
  }
};

const medicineKnowledge = {
  paracetamol: {
    purpose: "Used for fever and mild to moderate pain.",
    simple_explanation: "Helps reduce fever and body pain.",
    common_cautions: [
      "do not exceed the prescribed dose",
      "avoid combining with other paracetamol products"
    ]
  },
  acetaminophen: {
    purpose: "Used for fever and mild to moderate pain.",
    simple_explanation: "Another name for paracetamol; helps reduce fever and pain.",
    common_cautions: [
      "do not exceed the prescribed dose",
      "avoid combining with other acetaminophen products"
    ]
  },
  ibuprofen: {
    purpose: "Used for pain, fever, and inflammation.",
    simple_explanation: "Helps with swelling, pain, and fever.",
    common_cautions: ["take with food if advised", "avoid if a doctor told you to avoid NSAIDs"]
  },
  amoxicillin: {
    purpose: "Antibiotic used for some bacterial infections.",
    simple_explanation: "Helps fight certain bacterial infections.",
    common_cautions: ["complete the full course", "do not use for viral cold unless prescribed"]
  },
  azithromycin: {
    purpose: "Antibiotic used for some bacterial infections.",
    simple_explanation: "Helps fight certain bacterial infections.",
    common_cautions: ["take exactly as prescribed", "do not skip doses"]
  },
  cetirizine: {
    purpose: "Used for allergy symptoms such as sneezing, runny nose, or itching.",
    simple_explanation: "Helps reduce allergy symptoms.",
    common_cautions: ["may cause sleepiness", "avoid driving if drowsy"]
  },
  metformin: {
    purpose: "Used to help control blood sugar in type 2 diabetes.",
    simple_explanation: "Helps the body manage sugar levels.",
    common_cautions: ["take with meals if advised", "follow blood sugar monitoring advice"]
  },
  amlodipine: {
    purpose: "Used to treat high blood pressure.",
    simple_explanation: "Helps relax blood vessels and lower blood pressure.",
    common_cautions: ["take regularly", "do not stop suddenly without medical advice"]
  }
};

const frequencyPatterns = [
  [/\b1-0-1\b/i, "morning and night"],
  [/\b1-1-1\b/i, "morning, afternoon, and night"],
  [/\b1-0-0\b/i, "morning only"],
  [/\b0-0-1\b/i, "night only"],
  [/\bod\b/i, "once daily"],
  [/\bbd\b|\bbid\b/i, "twice daily"],
  [/\btds\b|\btid\b/i, "three times daily"],
  [/\bhs\b/i, "at bedtime"],
  [/\bsos\b|\bprn\b/i, "only when needed"]
];

function firstMatch(text, patterns) {
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[1].trim().replace(/[:\-\t ]+$/g, "");
    }
  }
  return "Unknown";
}

function detectRecordType(text) {
  const textLower = text.toLowerCase();
  if (/(tablet|tab|capsule|cap|syrup|rx|prescription)/.test(textLower)) {
    return "prescription";
  }
  if (/(what is|tell me about|disease|symptoms of)/.test(textLower)) {
    return "disease_question";
  }
  return "medical_text";
}

function extractFrequency(line) {
  for (const [pattern, meaning] of frequencyPatterns) {
    if (pattern.test(line)) {
      return meaning;
    }
  }
  return "not clearly mentioned";
}

function extractDuration(line) {
  const match = line.match(/\b(?:for\s*)?(\d+\s*(?:day|days|week|weeks|month|months))\b/i);
  return match ? match[1] : "not clearly mentioned";
}

function extractDosage(line) {
  const match = line.match(/\b(\d+(?:\.\d+)?\s*(?:mg|ml|mcg|g))\b/i);
  return match ? match[1] : "not clearly mentioned";
}

function extractMedicines(text) {
  const medicines = [];
  const seen = new Set();
  const knownNames = Object.keys(medicineKnowledge).join("|");
  const knownPattern = new RegExp(`\\b(${knownNames})\\b`, "gi");
  const fallbackPattern = /\b(?:tab|tablet|cap|capsule|syrup)\.?\s+([A-Za-z][A-Za-z0-9-]+)/gi;

  for (const line of text.split(/\r?\n/).map((item) => item.trim()).filter(Boolean)) {
    const matches = [
      ...Array.from(line.matchAll(knownPattern), (match) => match[1]),
      ...Array.from(line.matchAll(fallbackPattern), (match) => match[1])
    ];

    for (const rawName of matches) {
      const normalized = rawName.toLowerCase();
      if (seen.has(normalized)) {
        continue;
      }
      seen.add(normalized);
      const info = medicineKnowledge[normalized] || {};
      medicines.push({
        name: rawName.charAt(0).toUpperCase() + rawName.slice(1).toLowerCase(),
        dosage: extractDosage(line),
        frequency: extractFrequency(line),
        duration: extractDuration(line),
        purpose:
          info.purpose ||
          "Purpose is not available in the offline medicine database.",
        simple_explanation:
          info.simple_explanation ||
          "Medicine detected from the prescription text. Confirm details with a doctor or pharmacist.",
        common_cautions:
          info.common_cautions || [
            "use only as prescribed",
            "confirm unclear text with a doctor or pharmacist"
          ],
        source_line: line
      });
    }
  }
  return medicines;
}

function analyzeText(inputText) {
  const text = inputText.trim();
  const patient = {
    name: firstMatch(text, [
      /(?:patient\s*name|patient|name|prescribed\s*to)\s*[:\-]\s*([A-Za-z .]+)/i,
      /(?:mr|mrs|ms|miss)\.?\s+([A-Za-z .]+)/i
    ]),
    age: firstMatch(text, [/(?:age)\s*[:\-]?\s*(\d{1,3})\b/i]),
    gender: firstMatch(text, [/(?:sex|gender)\s*[:\-]?\s*(male|female|other|m|f)\b/i])
  };
  const provider = {
    doctor: firstMatch(text, [
      /(?:provider|doctor|dr\.?)\s*[:\-]?\s*([A-Za-z .]+)/i,
      /(Dr\.?\s+[A-Za-z .]+)/i
    ]),
    date: firstMatch(text, [
      /(?:date)\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})/i,
      /\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b/i
    ])
  };
  const conditions = Object.keys(diseaseKnowledge).filter((name) =>
    new RegExp(`\\b${name}\\b`, "i").test(text)
  );
  const diseaseInformation = conditions.map((name) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    ...diseaseKnowledge[name]
  }));
  const medicines = extractMedicines(text);
  const knownDetails = [
    ["Name", patient.name],
    ["Age", patient.age],
    ["Gender", patient.gender],
    ["Doctor", provider.doctor],
    ["Date", provider.date]
  ]
    .filter(([, value]) => value !== "Unknown")
    .map(([label, value]) => `${label}: ${value}`);
  const conditionSummary = diseaseInformation.length
    ? {
        plain_language_summary: `${diseaseInformation[0].name} was detected. ${diseaseInformation[0].overview}`,
        detected_conditions: diseaseInformation.map((condition) => condition.name),
        common_symptoms: diseaseInformation[0].common_symptoms,
        care_guidance: diseaseInformation[0].care_guidance,
        prevention_tips: diseaseInformation[0].prevention_tips,
        urgent_warning_signs: diseaseInformation[0].urgent_warning_signs
      }
    : {
        plain_language_summary:
          "No supported disease name was clearly detected. Review the text or enter symptoms such as fever, cough, cold, headache, diabetes, or hypertension.",
        detected_conditions: [],
        care_guidance: [
          "confirm the readable text with the original document",
          "consult a qualified clinician for diagnosis and treatment"
        ],
        urgent_warning_signs: [
          "breathing difficulty",
          "chest pain",
          "confusion or fainting",
          "severe or rapidly worsening symptoms"
        ]
      };
  const confidenceScore = Math.min(
    0.35 +
      (patient.name !== "Unknown" ? 0.15 : 0) +
      (provider.doctor !== "Unknown" ? 0.15 : 0) +
      (medicines.length ? 0.2 : 0) +
      (diseaseInformation.length ? 0.15 : 0),
    0.95
  );

  return {
    status: "success",
    data: {
      record_type: detectRecordType(text),
      input_text: text,
      patient,
      provider,
      date: provider.date,
      patient_summary: {
        identified_patient: patient.name,
        known_details: knownDetails.length
          ? knownDetails
          : ["No clear patient identity details found in the text."]
      },
      extracted_entities: conditions,
      medicines,
      disease_information: diseaseInformation,
      medical_analysis: {
        possible_condition: diseaseInformation[0]?.name || "Unknown",
        confidence_score: Number(confidenceScore.toFixed(2)),
        condition_summary: conditionSummary,
        medicine_summary: medicines.length
          ? {
              plain_language_summary: `${medicines.length} medicine item(s) were detected.`,
              instructions: medicines.map(
                (medicine) =>
                  `${medicine.name}: ${medicine.simple_explanation} Dose: ${medicine.dosage}; timing: ${medicine.frequency}; duration: ${medicine.duration}.`
              )
            }
          : {
              plain_language_summary: "No medicine name was clearly detected.",
              instructions: [
                "check the prescription image or typed text for medicine names",
                "ask a doctor or pharmacist before taking unclear medicines"
              ]
            },
        explanation_for_everyone:
          "This JSON is generated in the browser with an offline rule-based parser."
      },
      recommendation: {
        severity_level: diseaseInformation.length ? "review" : "unknown",
        care_plan: conditionSummary.care_guidance,
        urgent_warning_signs: conditionSummary.urgent_warning_signs,
        advice: [
          "Check the text against the original prescription.",
          "Follow the doctor's prescription exactly.",
          "Ask a doctor or pharmacist if medicine name, dose, or timing is unclear."
        ]
      }
    },
    meta: {
      model: "Offline Rule-Based Medical Parser",
      offline_mode: true,
      runtime: "Browser CPU",
      disclaimer:
        "Educational support only. Not a substitute for professional medical advice."
    }
  };
}

function processData() {
  const input = document.getElementById("inputText").value;
  const output = document.getElementById("output");

  if (!input.trim()) {
    output.textContent = "Enter medical text or a disease question to analyze.";
    return;
  }

  output.textContent = JSON.stringify(analyzeText(input), null, 2);
}

function loadExample() {
  document.getElementById("inputText").value = [
    "Patient Name: Asha Rao",
    "Age: 34",
    "Gender: Female",
    "Doctor: Dr Kumar",
    "Date: 12/05/2026",
    "Tab Paracetamol 500mg 1-0-1 for 3 days",
    "Symptoms: fever and headache"
  ].join("\n");
  processData();
}

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./sw.js").catch(() => {});
  });
}
