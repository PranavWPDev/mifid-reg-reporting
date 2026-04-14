export default function StatCard({ label, value }) {
  return (
    <div className="card p-4 rounded-xl">
      <p className="text-sm text-gray-400">{label}</p>
      <h2 className="text-2xl font-bold mt-1">{value}</h2>
    </div>
  );
}