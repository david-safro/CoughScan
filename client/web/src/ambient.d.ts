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

}