declare interface DiagnosisInfo {
    diagnosis: boolean,
    certainty: number,
    type: "cough" | "symptoms"
}
declare interface CoughTestOptions {
    ageRange: string,
    sex: "male" | "female" | "other",
    fever: boolean,
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
