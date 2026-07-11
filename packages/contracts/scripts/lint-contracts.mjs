import SwaggerParser from "@apidevtools/swagger-parser";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const contractsRoot = path.resolve(__dirname, "..");
const openApiPath = path.resolve(contractsRoot, "openapi/novel-factory.v1.yaml");
const schemaOrigin = "https://novelfactory.dev";

await SwaggerParser.validate(openApiPath, {
  resolve: {
    novelfactorySchemas: {
      order: 1,
      canRead(file) {
        return file.url.startsWith(`${schemaOrigin}/schemas/`);
      },
      async read(file) {
        const url = new URL(file.url);
        const localPath = path.resolve(contractsRoot, `.${url.pathname}`);
        return fs.readFile(localPath);
      },
    },
  },
});
console.log("contracts lint ok");
