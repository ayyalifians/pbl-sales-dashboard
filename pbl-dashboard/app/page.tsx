"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [salesData, setSalesData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Endpoint API FastAPI Kelompok 2 (Bisa disesuaikan dengan environment)
  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/data";

  useEffect(() => {
    // Simulasi pengambilan data dari backend
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        setSalesData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Gagal terhubung ke API:", err);
        setLoading(false);
      });
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center p-24 bg-gray-50 text-slate-800">
      <h1 className="text-4xl font-bold mb-2">Sales Dashboard - Kelompok 2</h1>
      <p className="mb-8 text-gray-500">Visualisasi Prediksi & Data Penjualan</p>
      
      <div className="w-full max-w-4xl bg-white p-6 rounded-xl shadow-lg border border-gray-100">
        <h2 className="text-xl font-semibold mb-4">Status Koneksi Database</h2>
        {loading ? (
          <p className="text-blue-500 animate-pulse">Menghubungkan ke API Backend...</p>
        ) : salesData.length > 0 ? (
           <p className="text-green-600 font-medium">✅ Data berhasil ditarik! Siap untuk integrasi grafik (Chart.js/D3).</p>
        ) : (
           <p className="text-red-500">Koneksi API gagal. Pastikan backend FastAPI sedang berjalan.</p>
        )}
      </div>
    </main>
  );
}