import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

export default defineConfig({
  site: "https://ravaniroshan.github.io/REI",
  base: "/REI",
  outDir: "../dist-docs",
  publicDir: "./public",
  integrations: [
    starlight({
      title: "REI",
      tagline: "Repository Evolution Intelligence",
      favicon: "/favicon.svg",
      logo: {
        src: "./src/assets/logo.svg",
        alt: "REI logo",
      },
      social: {
        github: "https://github.com/RavaniRoshan/REI",
      },
      sidebar: [
        {
          label: "Introduction",
          items: [
            { label: "Why REI?", slug: "introduction/motivation" },
            { label: "Quick Start", slug: "introduction/quick-start" },
          ],
        },
        {
          label: "Architecture",
          items: [
            { label: "System Overview", slug: "architecture/overview" },
            { label: "Static Graph", slug: "architecture/static-graph" },
            { label: "Coupling Graph", slug: "architecture/coupling-graph" },
            { label: "Prediction Engine", slug: "architecture/prediction-engine" },
          ],
        },
        {
          label: "Evaluation",
          items: [
            { label: "Methodology", slug: "evaluation/methodology" },
            { label: "Results", slug: "evaluation/results" },
            { label: "Ablation Studies", slug: "evaluation/ablation" },
          ],
        },
        {
          label: "CLI Reference",
          items: [
            { label: "Commands", slug: "cli/commands" },
            { label: "Configuration", slug: "cli/configuration" },
          ],
        },
        {
          label: "Development",
          items: [
            { label: "Contributing", slug: "development/contributing" },
            { label: "Project Structure", slug: "development/project-structure" },
          ],
        },
      ],
      editLink: {
        baseUrl: "https://github.com/RavaniRoshan/REI/edit/master/docs/",
      },
      lastUpdated: true,
    }),
  ],
});
