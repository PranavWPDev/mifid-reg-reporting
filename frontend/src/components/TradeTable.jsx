import StatusBadge from "./StatusBadge";

export default function TradeTable({ rows = [], variant, onAction }) {
  if (!rows.length) {
    return <div className="text-gray-400">No data available</div>;
  }

  return (
    <div className="overflow-auto rounded-xl border border-gray-700">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-800 text-gray-300">
          <tr>
            <th className="p-3">Trade</th>
            <th className="p-3">ISIN</th>
            <th className="p-3">Qty</th>
            <th className="p-3">Currency</th>
            <th className="p-3">Status</th>
            <th className="p-3">Confidence</th>
            {variant === "hitl" && <th className="p-3">Actions</th>}
          </tr>
        </thead>

        <tbody>
          {rows.map((row) => (
            <tr key={row.trade_id} className="border-t border-gray-700">
              <td className="p-3">{row.trade_id}</td>
              <td className="p-3">{row.isin}</td>
              <td className="p-3">{row.quantity}</td>
              <td className="p-3">{row.currency}</td>
              <td className="p-3">
                <StatusBadge status={row.final_status} />
              </td>
              <td className="p-3">
                {Math.round(row.decision_confidence * 100)}%
              </td>

              {variant === "hitl" && (
                <td className="p-3 flex gap-2">
                  <button
                    onClick={() => onAction(row, "APPROVED")}
                    className="bg-green-600 px-2 py-1 rounded text-xs"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => onAction(row, "REJECTED")}
                    className="bg-red-600 px-2 py-1 rounded text-xs"
                  >
                    Reject
                  </button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}