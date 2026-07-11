import SwaggerParser from "@apidevtools/swagger-parser";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const openApiPath = path.resolve(__dirname, "../openapi/novel-factory.v1.yaml");

await SwaggerParser.validate(openApiPath);
console.log("contracts lint ok");
