import { error } from "@sveltejs/kit";

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
    if (!params.id) throw error(404)

    const diagnosisInfo: DiagnosisInfo = {
        diagnosis: true,
        certainty: 76.5,
        type: "cough"
    };

    const coughTestOptions: CoughTestOptions = {
        age: 16,
        sex: "male",
        respiratoryCondition: "",
        feverMusclePain: true,
        healthStatus: ""
    };

    const symptomInputOptions: SymptomInputOptions = {

    }

    return {
        diagnosisInfo,
        coughTestOptions,
        symptomInputOptions
    }
}