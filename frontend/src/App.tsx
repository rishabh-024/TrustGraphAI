
import {
  ShieldCheck,
  Network,
  Activity,
  Database,
  ArrowUpRight,
} from "lucide-react";

const metrics = [
  {
    title: "Total Identities",
    value: "25",
    icon: Network,
    description: "Registered identities",
  },
  {
    title: "High-Risk Identities",
    value: "07",
    icon: ShieldCheck,
    description: "Require investigation",
  },
  {
    title: "Critical Assets",
    value: "12",
    icon: Database,
    description: "Protected resources",
  },
  {
    title: "Active Simulations",
    value: "00",
    icon: Activity,
    description: "Compromise simulations",
  },
];

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white px-8 py-5">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-slate-900 p-2 text-white">
              <ShieldCheck size={24} />
            </div>

            <div>
              <h1 className="text-xl font-bold">
                TrustGraph AI
              </h1>
              <p className="text-xs text-slate-500">
                Identity Risk Intelligence
              </p>
            </div>
          </div>

          <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
            Prototype Environment
          </span>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-8 py-10">
        <div className="mb-8">
          <p className="text-sm font-medium text-blue-600">
            SECURITY OVERVIEW
          </p>

          <h2 className="mt-2 text-3xl font-bold">
            Security Dashboard
          </h2>

          <p className="mt-2 text-slate-500">
            Monitor non-human identities and their potential
            security exposure.
          </p>
        </div>

        <section className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {metrics.map((metric) => {
            const Icon = metric.icon;

            return (
              <div
                key={metric.title}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-500">
                    {metric.title}
                  </span>

                  <Icon className="text-blue-600" size={22} />
                </div>

                <h3 className="mt-5 text-3xl font-bold">
                  {metric.value}
                </h3>

                <p className="mt-2 text-xs text-slate-400">
                  {metric.description}
                </p>
              </div>
            );
          })}
        </section>

        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-8">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">
              Platform Initialization
            </h3>

            <ArrowUpRight className="text-slate-400" />
          </div>

          <p className="mt-3 text-sm text-slate-500">
            TrustGraph AI development environment is initialized.
            Security intelligence modules will appear here as
            they are implemented.
          </p>

          <div className="mt-6 rounded-xl bg-slate-50 p-5">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              <span className="text-sm font-medium">
                Frontend initialized successfully
              </span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
