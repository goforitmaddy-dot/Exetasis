import React from "react";
import { Building, GraduationCap, Sprout, Factory, Stethoscope, HardHat } from "lucide-react";
import { useLanguageStore } from "../../store/useLanguageStore";

export const IndustryAdaptationSection: React.FC = () => {
  const { t } = useLanguageStore();

  const industries = [
    {
      id: "corporate",
      name: t("industries.corporate", "Corporate Offices"),
      desc: t(
        "industries.corporate_desc",
        "Desk topologies, cross-functional collaboration, and asynchronous flow."
      ),
      icon: <Building className="w-5 h-5 text-blue-400" />,
    },
    {
      id: "education",
      name: t("industries.education", "Educational Institutions"),
      desc: t(
        "industries.education_desc",
        "Campus labs, faculty research hubs, and collaborative lecture spaces."
      ),
      icon: <GraduationCap className="w-5 h-5 text-emerald-400" />,
    },
    {
      id: "agriculture",
      name: t("industries.agriculture", "Agriculture & Agritech"),
      desc: t(
        "industries.agriculture_desc",
        "Distributed field teams, sensor telemetry, and seasonal operational shifts."
      ),
      icon: <Sprout className="w-5 h-5 text-lime-400" />,
    },
    {
      id: "manufacturing",
      name: t("industries.manufacturing", "Manufacturing & Assembly"),
      desc: t(
        "industries.manufacturing_desc",
        "Assembly line ergonomics, shift handovers, and physical safety metrics."
      ),
      icon: <Factory className="w-5 h-5 text-amber-400" />,
    },
    {
      id: "healthcare",
      name: t("industries.healthcare", "Healthcare Systems"),
      desc: t(
        "industries.healthcare_desc",
        "Clinical care pods, on-call distribution fairness, and fatigue mitigation."
      ),
      icon: <Stethoscope className="w-5 h-5 text-rose-400" />,
    },
    {
      id: "construction",
      name: t("industries.construction", "Construction & Infrastructure"),
      desc: t(
        "industries.construction_desc",
        "Job site zones, safety compliance checkpoints, and contractor coordination."
      ),
      icon: <HardHat className="w-5 h-5 text-yellow-400" />,
    },
  ];

  return (
    <section id="industries" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-t border-slate-800/80">
      <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-xs font-semibold uppercase tracking-wider text-indigo-400">
          {t("industries.badge", "Universal Adaptability")}
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          {t("industries.title", "Engineered for Every Work Environment")}
        </h2>
        <p className="text-slate-400 text-sm sm:text-base">
          {t(
            "industries.subtitle",
            "From corporate office towers to field operations, Exetasis adapts its sensory models to your operational reality."
          )}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {industries.map((ind) => (
          <div
            key={ind.id}
            className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700/80 transition-all hover:bg-slate-900/90 flex items-start gap-4"
          >
            <div className="w-10 h-10 rounded-lg bg-slate-800/80 flex items-center justify-center flex-shrink-0 border border-slate-700/60 shadow-sm">
              {ind.icon}
            </div>
            <div>
              <h3 className="font-bold text-white text-sm">{ind.name}</h3>
              <p className="text-xs text-slate-400 mt-1 leading-relaxed">{ind.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
