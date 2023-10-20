import { error } from "@sveltejs/kit";
import type { PageData } from "./$types.js";

/** @type {import('./$types').PageLoad} */
export async function load({ params }) {
    if (!params.data) throw error(404)

    const pageData: PageData = JSON.parse(decodeURIComponent(params.data))

    return pageData;
}