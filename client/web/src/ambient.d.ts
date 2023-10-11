declare interface DiagnosisInfo {
    diagnosis: boolean,
    certainty: number,
    type: "cough" | "symptoms"
}
declare interface CoughTestOptions {
    age: number,
    sex: "male" | "female" | "other",
    respiratoryCondition: string,
    feverMusclePain: boolean,
    healthStatus: string
}
declare interface SymptomInputOptions {
    fever: boolean,
    tiredness: boolean,
    dryCough: boolean,
    difficultyInBreathing: boolean,
    soreThroat: boolean,
    pains: boolean,
    nasalCongestion: boolean,
    runnyNose: boolean,
    diarrhea: boolean,
    noneSymptom: boolean,
    noneExperiencing: boolean,
    ageGroup: "0-9" | "10-19" | "20-24" | "25-59" | "60+",
    gender: "male" | "female" | "transgender",
    contactHistory: "dont-know" | "no" | "yes"
}
