"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [salesData, setSalesData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Memanggil raw data JSON langsung dari folder public Vercel
    fetch("/sales_data.json")
      .then((res) => {
        if (!res.ok) throw new Error("Gagal mengambil data statis");
        return res.json();
      })
      .then((data) => {
        setSalesData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error:", err);
        setLoading(false);
      });
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center p-24 bg-gray-50 text-slate-800">
      <h1 className="text-4xl font-bold mb-2">Sales Dashboard - Kelompok 2</h1>
      <p className="mb-8 text-gray-500">Visualisasi Prediksi & Data Penjualan Superstore</p>
      
      <div className="w-full max-w-4xl bg-white p-6 rounded-xl shadow-lg border border-gray-100">
        <h2 className="text-xl font-semibold mb-4">Status Integrasi Data</h2>
        {loading ? (
          <p className="text-blue-500 animate-pulse">Memuat raw dataset...</p>
        ) : salesData.length > 0 ? (
          <div>
            <p className="text-green-600 font-medium mb-4">✅ Data berhasil ditarik! Menampilkan {salesData.length} sampel teratas.</p>
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b">
                  <th className="py-2">Order ID</th>
                  <th className="py-2">Kategori</th>
                  <th className="py-2">Sales ($)</th>
                </tr>
              </thead>
              <tbody>
                {salesData.map((item, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    <td className="py-2">{item.id}</td>
                    <td className="py-2">{item.kategori}</td>
                    <td className="py-2">{item.sales}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
           <p className="text-red-500">Gagal memuat data.</p>
        )}
      </div>
    </main>
  );
}