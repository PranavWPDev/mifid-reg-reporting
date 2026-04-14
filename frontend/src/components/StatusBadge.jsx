export default function StatusBadge({ status }) {
  const map = {
    PASS: "bg-green-500/20 text-green-400",
    REJECTED: "bg-red-500/20 text-red-400",
    HITL: "bg-yellow-500/20 text-yellow-400",
  };

  return (
    <span className={`px-3 py-1 rounded-full text-xs ${map[status] || "bg-gray-500/20"}`}>
      {status}
    </span>
  );
}