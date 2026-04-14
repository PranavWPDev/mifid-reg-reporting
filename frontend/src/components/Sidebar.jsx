export default function Sidebar({ activeTab, setActiveTab }) {
  const tabs = ["input", "dashboard", "validation", "risk", "compliance", "hitl", "report"];

  return (
    <div className="w-60 p-4 border-r border-gray-800 hidden lg:block">
      <h2 className="text-lg font-bold mb-6">MiFID AI</h2>

      {tabs.map((t) => (
        <div
          key={t}
          onClick={() => setActiveTab(t)}
          className={`p-2 rounded cursor-pointer ${
            activeTab === t ? "bg-blue-600" : "hover:bg-gray-700"
          }`}
        >
          {t.toUpperCase()}
        </div>
      ))}
    </div>
  );
}