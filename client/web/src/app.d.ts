// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		interface PageData {
			diagnosisInfo: DiagnosisInfo
			coughTestOptions?: CoughTestOptions
			symptomInputOptions?: SymptomInputOptions
		}
		// interface Platform {}
	}
}

export {};
