"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [salesData, setSalesData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // GANTI URL ini dengan URL asli dari Railway kelompok Anda
  // Pastikan menyertakan path endpoint yang tepat (misal: /api/forecast atau /sales)
  const RAILWAY_API_URL = "https://pbl-sales-dashboard-production.up.railway.app";

  useEffect(() => {
    // Memanggil API Live Publik dari Railway
    fetch(RAILWAY_API_URL)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Gagal mengambil data dari API (Status: ${res.status})`);
        }
        return res.json();
      })
      .then((data) => {
        // CATATAN: Pastikan API Anda mengembalikan data berformat Array/List [{}, {}, {}]
        // Jika formatnya berbeda, sesuaikan baris di bawah ini (misal: data.results)
        setSalesData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error:", err);
        setErrorMessage(err.message);
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
          <p className="text-blue-500 animate-pulse">Memuat data live dari Railway API...</p>
        ) : errorMessage ? (
          <div className="p-4 bg-red-50 text-red-700 rounded-lg">
            <p className="font-medium">⚠️ Terjadi Kesalahan Koneksi:</p>
            <p className="text-sm">{errorMessage}</p>
            <p className="text-xs mt-2 text-gray-400">Tips: Pastikan CORS sudah diaktifkan pada file main.py FastAPI.</p>
          </div>
        ) : salesData.length > 0 ? (
          <div>
            <p className="text-green-600 font-medium mb-4">
              ✅ Data Live berhasil ditarik dari Railway! Menampilkan {salesData.length} sampel teratas.
            </p>
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b">
                  {/* Sesuaikan nama kolom header ini dengan key JSON dari API Anda */}
                  <th className="py-2">Order ID</th>
                  <th className="py-2">Kategori</th>
                  <th className="py-2">Sales ($)</th>
                </tr>
              </thead>
              <tbody>
                {salesData.map((item, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    {/* ⚠️ PENTING: Ganti item.id, item.kategori, item.sales di bawah ini 
                        sesuaikan dengan nama key huruf kecil/besar dari JSON FastAPI Anda */}
                    <td className="py-2">{item.id || item.order_id || index}</td>
                    <td className="py-2">{item.kategori || item.category}</td>
                    <td className="py-2">{item.sales || item.prediksi_penjualan}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-red-500">Gagal memuat data atau data kosong.</p>
        )}
      </div>
    </main>
  );
}