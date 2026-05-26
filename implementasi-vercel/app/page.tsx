export default function Home() {
  const salesData = [
    { id: "CA-2023-152156", kategori: "Furniture", sales: 261.96, profit: 41.91 },
    { id: "CA-2023-138688", kategori: "Office Supplies", sales: 14.56, profit: 3.12 },
    { id: "US-2023-108966", kategori: "Technology", sales: 957.58, profit: 383.03 },
    { id: "CA-2023-115812", kategori: "Furniture", sales: 48.86, profit: 14.16 },
    { id: "CA-2023-114412", kategori: "Office Supplies", sales: 15.55, profit: 5.44 }
  ];

  const totalSales = salesData.reduce((acc, item) => acc + item.sales, 0);
  const totalProfit = salesData.reduce((acc, item) => acc + item.profit, 0);

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800">
          PBL Sales Dashboard
        </h1>

        <p className="text-gray-500 mt-2">
          Dashboard monitoring penjualan dan profit bisnis
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-gray-500">Total Sales</h2>

          <p className="text-3xl font-bold text-blue-600 mt-2">
            ${totalSales.toFixed(2)}
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-gray-500">Total Profit</h2>

          <p className="text-3xl font-bold text-green-600 mt-2">
            ${totalProfit.toFixed(2)}
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-gray-500">Total Transactions</h2>

          <p className="text-3xl font-bold text-purple-600 mt-2">
            {salesData.length}
          </p>
        </div>

      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl shadow p-6 overflow-x-auto">

        <h2 className="text-2xl font-semibold mb-4">
          Sales Transactions
        </h2>

        <table className="w-full border-collapse">

          <thead>
            <tr className="border-b bg-gray-50">
              <th className="text-left p-3">Order ID</th>
              <th className="text-left p-3">Category</th>
              <th className="text-left p-3">Sales</th>
              <th className="text-left p-3">Profit</th>
            </tr>
          </thead>

          <tbody>
            {salesData.map((item) => (
              <tr
                key={item.id}
                className="border-b hover:bg-gray-50 transition"
              >
                <td className="p-3">{item.id}</td>
                <td className="p-3">{item.kategori}</td>
                <td className="p-3">${item.sales}</td>
                <td className="p-3 text-green-600 font-medium">
                  ${item.profit}
                </td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </main>
  );
}