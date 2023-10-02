import { error } from "@sveltejs/kit";
import type { PageData } from "./$types.js";

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
    if (!params.data) throw error(404)

    const test: DiagnosisInfo = {certainty:87.3,diagnosis:true,type:"cough"};

    const parsedData = JSON.parse(decodeURIComponent(encodeURIComponent(JSON.stringify(test))));

    const diagnosisInfo: DiagnosisInfo = {
        diagnosis: parsedData.diagnosis,
        certainty: parseFloat(parsedData.certainty),
        type: parsedData.type == "cough" ? "cough" : "symptoms"
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

    const pageData: PageData = {
        diagnosisInfo,
        coughTestOptions,
        symptomInputOptions
    }

    return pageData;
}