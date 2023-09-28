declare interface DiagnosisInfo {
    diagnosis: boolean,
    certainty: number
}
declare interface UserOptions {
    age: number,
    sex: "male" | "female" | "other",
    respiratoryCondition: string,
    feverMusclePain: boolean,
    healthStatus: string
}