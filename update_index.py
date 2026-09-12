# Helper script to write the complete single-file index.html
import os

html_head_and_body = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV Scentia Ultimacos - System SPK V6.0</title>
    <meta name="description" content="Sistem SPK & Costing Formulasi Parfum CV Scentia Ultimacos dengan integrasi Supabase" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
        * { font-family: 'Inter', sans-serif; }
        body { background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); min-height: 100vh; }
        
        .a4-page { width: 210mm; height: 297mm; padding: 8mm; background: white; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }
        .a4-page-landscape { width: 297mm; height: 210mm; padding: 8mm; background: white; box-sizing: border-box; display: flex; flex-direction: column; justify-content: space-between; overflow: hidden; }
        #pdf-render-area { position: absolute; left: -9999px; top: -9999px; }

        .status-badge { transition: all 0.2s; font-size: 10px; font-weight: 700; padding: 4px 12px; border-radius: 9999px; display: inline-block; }
        .status-badge.menunggu { background: #fef3c7; color: #92400e; }
        .status-badge.sudah { background: #dbeafe; color: #1e40af; }
        .status-badge.siap { background: #d1fae5; color: #065f46; }
        .status-badge.produksi { background: #fce4ec; color: #b71c1c; }
        .status-badge.selesai { background: #e8f5e9; color: #1b5e20; }
        .status-badge.revisi { background: #fff3e0; color: #bf360c; }
        .status-badge.arsip { background: #e2e8f0; color: #475569; }

        .card-hover { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .card-hover:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,0.08); }

        .cek-item { transition: all 0.2s; border-radius: 10px; }
        .cek-item:hover { background: #f8fafc; }
        .cek-item.checked { background: #f0fdf4; border-color: #86efac; }

        .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; animation: fadeIn 0.2s; }
        .modal-content { background: white; border-radius: 20px; padding: 28px; max-width: 800px; width: 92%; max-height: 85vh; overflow-y: auto; animation: slideUp 0.3s; box-shadow: 0 25px 60px rgba(0,0,0,0.2); }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

        .pdf-header { border-bottom: 3px solid #1e293b; padding-bottom: 8px; }
        .pdf-footer { border-top: 2px solid #e2e8f0; padding-top: 8px; font-size: 8px; color: #94a3b8; }
        .pdf-table { width: 100%; border-collapse: collapse; font-size: 8px; }
        .pdf-table th { background: #1e293b; color: white; padding: 4px 6px; text-align: left; border: 1px solid #1e293b; }
        .pdf-table td { padding: 4px 6px; border: 1px solid #cbd5e1; }
        .pdf-table tr:nth-child(even) { background: #f8fafc; }
        .pdf-table .total-row { background: #dbeafe !important; font-weight: bold; }

        .gradient-header { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); }
        .gradient-primary { background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); }
        .gradient-success { background: linear-gradient(135deg, #059669 0%, #10b981 100%); }
        .gradient-warning { background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); }
        .gradient-danger { background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%); }
        .gradient-amber { background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); }
        .gradient-purple { background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%); }
        .gradient-teal { background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%); }
        .gradient-pink { background: linear-gradient(135deg, #db2777 0%, #f472b6 100%); }
        .gradient-slate { background: linear-gradient(135deg, #475569 0%, #64748b 100%); }

        .tab-btn { transition: all 0.3s; border-radius: 12px 12px 0 0; padding: 12px 20px; font-weight: 600; font-size: 13px; color: #64748b; position: relative; }
        .tab-btn:hover { color: #4f46e5; background: rgba(79,70,229,0.05); }
        .tab-btn.active { color: #4f46e5; background: white; box-shadow: 0 -2px 10px rgba(79,70,229,0.08); }
        .tab-btn.active::after { content: ''; position: absolute; bottom: -1px; left: 20%; right: 20%; height: 3px; background: linear-gradient(90deg, #4f46e5, #7c3aed); border-radius: 10px; }

        .variant-card { border-left: 4px solid #4f46e5; }
        .stok-sisa-card { border-left: 4px solid #8b5cf6; }

        .laporan-preview { max-height: 500px; overflow-y: auto; }
        .laporan-preview table { font-size: 13px; }
        .laporan-preview table th { background: #1e293b; color: white; padding: 8px 12px; text-align: left; }
        .laporan-preview table td { padding: 8px 12px; border-bottom: 1px solid #e2e8f0; }
        .laporan-preview table tr:hover { background: #f8fafc; }
        .laporan-preview table .total-row { background: #dbeafe !important; font-weight: bold; }

        .stok-sisa-table { font-size: 13px; }
        .stok-sisa-table th { background: #7c3aed; color: white; padding: 8px 12px; text-align: left; }
        .stok-sisa-table td { padding: 8px 12px; border-bottom: 1px solid #e2e8f0; }
        .stok-sisa-table tr:hover { background: #faf5ff; }
        .stok-sisa-table .total-row { background: #ede9fe !important; font-weight: bold; }
        
        .tab-btn.hidden-tab { display: none !important; }
        
        .access-checkbox-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 8px;
        }
        .access-checkbox-grid label {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 10px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .access-checkbox-grid label:hover {
            background: #eef2ff;
            border-color: #818cf8;
        }
        .access-checkbox-grid label.checked {
            background: #eef2ff;
            border-color: #6366f1;
        }
        .access-checkbox-grid input[type="checkbox"] {
            width: 16px;
            height: 16px;
            accent-color: #6366f1;
            cursor: pointer;
        }

        .user-table td { vertical-align: middle; padding: 10px 12px; }
        .user-table .password-cell { font-family: 'Courier New', monospace; font-weight: 600; color: #1e293b; letter-spacing: 0.5px; background: #f1f5f9; border-radius: 6px; padding: 4px 10px; display: inline-block; }

        .filter-input { border: 1px solid #e2e8f0; padding: 8px 14px; border-radius: 12px; font-size: 13px; outline: none; transition: all 0.2s; }
        .filter-input:focus { border-color: #6366f1; ring: 2px solid #818cf8; }
        .filter-select { border: 1px solid #e2e8f0; padding: 8px 14px; border-radius: 12px; font-size: 13px; outline: none; background: white; cursor: pointer; }
        .filter-select:focus { border-color: #6366f1; }

        .archive-item { border-left: 4px solid #94a3b8; }
        .archive-bj { border-left: 4px solid #10b981; }
        .archive-ss { border-left: 4px solid #8b5cf6; }
    </style>
</head>
<body>

    <!-- ================= LOGIN ================= -->
    <div id="page-login" class="min-h-screen flex items-center justify-center p-4" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);">
        <div class="bg-white/10 backdrop-blur-xl p-8 sm:p-10 rounded-3xl shadow-2xl w-full max-w-md border border-white/10 fade-in">
            <div class="text-center space-y-3">
                <div class="inline-block p-4 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl text-3xl shadow-lg">🧪</div>
                <h1 class="text-2xl font-extrabold text-white tracking-tight">CV Scentia Ultimacos</h1>
                <p class="text-sm text-slate-400 font-medium">Sistem SPK & Costing V6.0</p>
            </div>
            <form onsubmit="handleLogin(event)" class="space-y-5 mt-8">
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5">Username</label>
                    <input type="text" id="login-user" required placeholder="Masukkan username" class="w-full bg-white/10 border border-white/20 text-white placeholder-slate-400 p-3.5 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5">Password</label>
                    <input type="password" id="login-pass" required placeholder="Masukkan password" class="w-full bg-white/10 border border-white/20 text-white placeholder-slate-400 p-3.5 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                </div>
                <button type="submit" id="btn-login-submit" class="w-full bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold py-3.5 rounded-xl text-sm shadow-lg hover:shadow-indigo-500/30 transition-all hover:scale-[1.02]">🔑 Masuk Dashboard</button>
            </form>
        </div>
    </div>

    <!-- ================= DASHBOARD ================= -->
    <div id="page-dashboard" class="hidden p-4 sm:p-6 max-w-7xl mx-auto space-y-4 sm:space-y-6">
        
        <!-- Header -->
        <div class="gradient-header rounded-2xl shadow-xl p-4 sm:p-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border border-white/10">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg">SU</div>
                <div>
                    <h1 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">CV Scentia Ultimacos</h1>
                    <p class="text-slate-400 text-xs font-medium">System Formulasi & Calculation Costing V6.0</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <span class="text-xs text-slate-400 hidden sm:inline" id="header-user-info">👤 Admin</span>
                <button onclick="handleLogout()" class="bg-rose-600 hover:bg-rose-700 text-white px-4 py-2 rounded-xl font-bold text-xs shadow-lg hover:shadow-rose-500/30 transition-all hover:scale-[1.02]">🚪 Logout</button>
            </div>
        </div>

        <!-- Tab Navigation -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200/60 overflow-x-auto">
            <div class="flex px-2 sm:px-4 gap-0.5 sm:gap-1 whitespace-nowrap">
                <button onclick="switchTab('spk')" id="tab-spk" class="tab-btn active">📋 Input SPK</button>
                <button onclick="switchTab('harga')" id="tab-harga" class="tab-btn">💰 Master</button>
                <button onclick="switchTab('history')" id="tab-history" class="tab-btn">📂 Riwayat SPK</button>
                <button onclick="switchTab('gudang')" id="tab-gudang" class="tab-btn">🏭 Gudang</button>
                <button onclick="switchTab('produksi')" id="tab-produksi" class="tab-btn">⚙️ Produksi</button>
                <button onclick="switchTab('barangjadi')" id="tab-barangjadi" class="tab-btn">📦 Barang Jadi</button>
                <button onclick="switchTab('stoksisa')" id="tab-stoksisa" class="tab-btn">📊 Stok Sisa</button>
                <button onclick="switchTab('archive')" id="tab-archive" class="tab-btn">🗄️ Arsip SPK</button>
                <button onclick="switchTab('archivebj')" id="tab-archivebj" class="tab-btn">📦 Arsip BJ</button>
                <button onclick="switchTab('archivess')" id="tab-archivess" class="tab-btn">📊 Arsip SS</button>
            </div>
        </div>

        <!-- TAB INPUT SPK -->
        <div id="page-spk" class="space-y-4 fade-in">
            <form onsubmit="simpanSPKUtama(event)" class="space-y-4">
                <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                    <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                        <h2 class="text-sm font-bold text-indigo-900">📌 Data Utama SPK</h2>
                        <input type="hidden" id="edit-spk-id" value="">
                        <span id="edit-mode-label" class="hidden text-xs font-bold text-amber-600 bg-amber-50 px-3 py-1 rounded-full border border-amber-200">✏️ Mode Edit</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-1">Nomor SPK</label>
                            <input type="text" id="spk-nomor" required placeholder="SPK/2026/001" class="w-full border border-slate-200 p-3 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-1">Nama Brand</label>
                            <input type="text" id="spk-brand" required placeholder="Kahfian" class="w-full border border-slate-200 p-3 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-1">Tanggal SPK</label>
                            <input type="date" id="spk-tanggal" required class="w-full border border-slate-200 p-3 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition">
                        </div>
                    </div>
                </div>

                <div id="container-varian" class="space-y-4"></div>

                <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200/60 flex flex-col md:flex-row justify-between items-center gap-4">
                    <button type="button" onclick="tambahVarianBaru()" class="bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-bold px-5 py-3 rounded-xl text-sm shadow-lg hover:shadow-emerald-500/30 transition-all hover:scale-[1.02] w-full md:w-auto">➕ Tambah Varian</button>
                    <div class="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
                        <div id="status-validasi-global" class="text-xs font-bold text-rose-600 text-center sm:text-left"></div>
                        <button type="submit" id="btn-simpan-spk" class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold px-8 py-3 rounded-xl text-sm shadow-lg hover:shadow-indigo-500/30 transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 w-full sm:w-auto">💾 Simpan SPK</button>
                        <button type="button" onclick="batalEditSPK()" id="btn-batal-edit" class="hidden bg-slate-400 hover:bg-slate-500 text-white font-bold px-4 py-3 rounded-xl text-sm shadow transition w-full sm:w-auto">❌ Batal Edit</button>
                    </div>
                </div>
            </form>
        </div>

        <!-- TAB MASTER -->
        <div id="page-harga" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <h2 class="text-sm font-bold text-slate-800">📏 Master Satuan</h2>
                    <button onclick="tambahMasterSatuan()" class="bg-gradient-to-r from-teal-500 to-cyan-500 text-white font-bold px-4 py-2 rounded-xl text-xs shadow hover:shadow-teal-500/30 transition">+ Tambah Satuan</button>
                </div>
                <div id="list-satuan-master" class="flex flex-wrap gap-2"></div>
            </div>
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <h2 class="text-sm font-bold text-indigo-900">🧬 Template Formulasi</h2>
                    <button onclick="tambahTemplateFormulasiBaru()" class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold px-4 py-2 rounded-xl text-xs shadow hover:shadow-indigo-500/30 transition">+ Tambah</button>
                </div>
                <div id="list-template-formulasi" class="space-y-3"></div>
            </div>
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <h2 class="text-sm font-bold text-slate-800">🧪 Harga Bahan Baku</h2>
                    <button onclick="tambahMasterBahanBaru()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-4 py-2 rounded-xl text-xs shadow transition">+ Tambah</button>
                </div>
                <div id="list-harga-master" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3"></div>
            </div>
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <h2 class="text-sm font-bold text-amber-800">📦 Harga Box Kemasan</h2>
                    <button onclick="tambahMasterBoxBaru()" class="bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold px-4 py-2 rounded-xl text-xs shadow hover:shadow-amber-500/30 transition">+ Tambah</button>
                </div>
                <div id="list-box-master" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3"></div>
            </div>
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <h2 class="text-sm font-bold text-purple-800">🏷️ Harga Sticker</h2>
                    <button onclick="tambahMasterStickerBaru()" class="bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold px-4 py-2 rounded-xl text-xs shadow hover:shadow-purple-500/30 transition">+ Tambah</button>
                </div>
                <div id="list-sticker-master" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3"></div>
            </div>
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <h2 class="text-sm font-bold text-slate-800">🛠️ Ongkos Kerja</h2>
                    <button onclick="tambahMasterOngkosBaru()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-4 py-2 rounded-xl text-xs shadow transition">+ Tambah</button>
                </div>
                <div id="list-ongkos-kerja" class="grid grid-cols-1 sm:grid-cols-2 gap-3"></div>
            </div>
            
            <!-- USER MANAGEMENT -->
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4 mt-4" id="user-management-section">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                        <h2 class="text-sm font-bold text-rose-800">👥 Manajemen User & Hak Akses</h2>
                        <p class="text-[10px] text-slate-400 mt-0.5">Kelola user, role, dan hak akses menu. Password terlihat jelas untuk admin.</p>
                    </div>
                    <span class="text-[10px] font-bold bg-rose-100 text-rose-800 px-3 py-1 rounded-full">🔒 Admin Only</span>
                </div>
                <div id="user-management-container"></div>
            </div>
        </div>

        <!-- TAB RIWAYAT SPK -->
        <div id="page-history" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <h2 class="text-sm font-bold text-slate-800">📂 Daftar SPK Tersimpan</h2>
                    <span id="label-total-history" class="text-xs font-bold bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full">0 SPK</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full text-left text-sm border-collapse">
                        <thead><tr class="bg-slate-50 text-xs uppercase border-b border-slate-200">
                            <th class="p-3 font-bold text-slate-600">No. SPK</th>
                            <th class="p-3 font-bold text-slate-600">Brand</th>
                            <th class="p-3 font-bold text-slate-600">Tanggal</th>
                            <th class="p-3 text-center font-bold text-slate-600">Varian</th>
                            <th class="p-3 text-right font-bold text-slate-600">Total PO</th>
                            <th class="p-3 text-center font-bold text-slate-600">Status</th>
                            <th class="p-3 text-center font-bold text-slate-600">Aksi</th>
                        </tr></thead>
                        <tbody id="tabel-history" class="divide-y divide-slate-100"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB GUDANG -->
        <div id="page-gudang" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                        <h2 class="text-sm font-bold text-indigo-900">🏭 Gudang - Cek Ketersediaan</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Ceklist bahan baku, botol, box, dan sticker</p>
                    </div>
                    <span id="label-total-gudang" class="text-xs font-bold bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full">0 SPK</span>
                </div>
                <div id="list-spk-gudang" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3"></div>
                <div id="detail-spk-gudang" class="hidden border-t border-slate-200 pt-4 mt-2">
                    <div class="flex justify-between items-center border-b border-slate-100 pb-3 mb-3">
                        <div><h3 class="text-sm font-bold text-slate-800" id="gudang-spk-title">SPK: -</h3><p class="text-xs text-slate-500" id="gudang-spk-brand">Brand: -</p></div>
                        <span id="gudang-status-badge" class="status-badge menunggu">⏳ Menunggu Cek</span>
                    </div>
                    <div id="gudang-bahan-list" class="space-y-2"></div>
                    <div class="flex justify-end mt-4 pt-3 border-t border-slate-200">
                        <button onclick="lanjutProduksi()" id="btn-lanjut-produksi" disabled class="bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-bold px-6 py-2.5 rounded-xl text-sm shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:scale-[1.02]">🏭 LANJUT KE PRODUKSI</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB PRODUKSI -->
        <div id="page-produksi" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                        <h2 class="text-sm font-bold text-slate-800">⚙️ Manajemen Produksi</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Input barang jadi, rusak, dan bahan sisa per varian</p>
                    </div>
                    <span id="label-total-produksi" class="text-xs font-bold bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full">0 SPK</span>
                </div>
                <div id="list-spk-produksi" class="space-y-3"></div>
            </div>
        </div>

        <!-- TAB BARANG JADI -->
        <div id="page-barangjadi" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                        <h2 class="text-sm font-bold text-emerald-800">📦 Manajemen Barang Jadi</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Filter, cari, dan urutkan stok barang jadi</p>
                    </div>
                    <span id="label-total-barangjadi" class="text-xs font-bold bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full">0 Item</span>
                </div>
                
                <div class="flex flex-wrap gap-3 items-center bg-slate-50 p-3 rounded-xl border border-slate-200">
                    <input type="text" id="bj-search" placeholder="🔍 Cari brand / varian..." oninput="renderBarangJadi()" class="filter-input flex-1 min-w-[150px]">
                    <select id="bj-filter-brand" onchange="renderBarangJadi()" class="filter-select min-w-[120px]">
                        <option value="">Semua Brand</option>
                    </select>
                    <select id="bj-sort" onchange="renderBarangJadi()" class="filter-select min-w-[140px]">
                        <option value="newest">🕐 Terbaru</option>
                        <option value="oldest">🕐 Terlama</option>
                        <option value="name-asc">📝 Nama A-Z</option>
                        <option value="name-desc">📝 Nama Z-A</option>
                        <option value="qty-desc">📊 Stok Tertinggi</option>
                        <option value="qty-asc">📊 Stok Terendah</option>
                    </select>
                    <button onclick="renderBarangJadi()" class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-xl text-sm font-bold transition">🔄 Refresh</button>
                </div>
                
                <div id="list-barangjadi" class="space-y-3"></div>
            </div>
        </div>

        <!-- TAB STOK SISA -->
        <div id="page-stoksisa" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                        <h2 class="text-sm font-bold text-purple-800">📊 Stok Sisa Produksi</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Laporan bahan baku sisa dari produksi yang sudah selesai</p>
                    </div>
                    <span id="label-total-stoksisa" class="text-xs font-bold bg-purple-100 text-purple-800 px-3 py-1 rounded-full">0 Laporan</span>
                </div>

                <div id="realtime-stok-sisa" class="hidden border border-purple-200 rounded-xl overflow-hidden">
                    <div class="bg-purple-800 text-white px-4 py-2.5 flex justify-between items-center">
                        <span class="text-xs font-bold uppercase tracking-wider">📊 Realtime Stok Sisa Bahan Baku</span>
                        <span class="text-[10px] bg-purple-600 px-3 py-1 rounded-full" id="label-total-sisa-realtime">0 Total</span>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm border-collapse stok-sisa-table">
                            <thead>
                                <tr class="bg-purple-100">
                                    <th class="p-2.5 border-b border-purple-200 font-bold text-purple-900">Bahan Baku</th>
                                    <th class="p-2.5 border-b border-purple-200 font-bold text-purple-900">Brand</th>
                                    <th class="p-2.5 border-b border-purple-200 font-bold text-purple-900">No. SPK</th>
                                    <th class="p-2.5 border-b border-purple-200 font-bold text-purple-900 text-right">Sisa</th>
                                    <th class="p-2.5 border-b border-purple-200 font-bold text-purple-900 text-center">Tanggal</th>
                                    <th class="p-2.5 border-b border-purple-200 font-bold text-purple-900 text-center">Aksi</th>
                                </tr>
                            </thead>
                            <tbody id="table-realtime-sisa"></tbody>
                        </table>
                    </div>
                </div>

                <div class="border-t border-purple-200 pt-4 mt-2">
                    <div class="flex justify-between items-center mb-3">
                        <h3 class="text-sm font-bold text-purple-800">📋 Daftar Laporan Stok Sisa per SPK</h3>
                        <span class="text-xs font-bold bg-purple-100 text-purple-800 px-3 py-1 rounded-full" id="label-total-stoksisa-list">0</span>
                    </div>
                    <div id="list-stoksisa" class="space-y-3"></div>
                </div>
            </div>
        </div>

        <!-- TAB ARCHIVE SPK -->
        <div id="page-archive" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                        <h2 class="text-sm font-bold text-slate-700">🗄️ Arsip SPK</h2>
                        <p class="text-xs text-slate-500 mt-0.5">SPK yang sudah diarsipkan. Bisa dikembalikan atau dihapus permanen.</p>
                    </div>
                    <span id="label-total-archive" class="text-xs font-bold bg-slate-100 text-slate-700 px-3 py-1 rounded-full">0 Arsip</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full text-left text-sm border-collapse">
                        <thead><tr class="bg-slate-50 text-xs uppercase border-b border-slate-200">
                            <th class="p-3 font-bold text-slate-600">No. SPK</th>
                            <th class="p-3 font-bold text-slate-600">Brand</th>
                            <th class="p-3 font-bold text-slate-600">Tanggal</th>
                            <th class="p-3 text-center font-bold text-slate-600">Varian</th>
                            <th class="p-3 text-right font-bold text-slate-600">Total PO</th>
                            <th class="p-3 text-center font-bold text-slate-600">Aksi</th>
                        </tr></thead>
                        <tbody id="tabel-archive" class="divide-y divide-slate-100"></tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB ARCHIVE BARANG JADI -->
        <div id="page-archivebj" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                        <h2 class="text-sm font-bold text-emerald-800">📦 Arsip Barang Jadi</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Barang jadi yang sudah diarsipkan. Bisa dikembalikan atau dihapus permanen.</p>
                    </div>
                    <span id="label-total-archivebj" class="text-xs font-bold bg-slate-100 text-slate-700 px-3 py-1 rounded-full">0 Arsip</span>
                </div>
                <div id="list-archivebj" class="space-y-3"></div>
            </div>
        </div>

        <!-- TAB ARCHIVE STOK SISA -->
        <div id="page-archivess" class="space-y-4 hidden fade-in">
            <div class="bg-white p-4 sm:p-6 rounded-2xl shadow-sm border border-slate-200/60 space-y-4">
                <div class="flex justify-between items-center border-b border-slate-100 pb-3">
                    <div>
                        <h2 class="text-sm font-bold text-purple-800">📊 Arsip Stok Sisa</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Laporan stok sisa yang sudah diarsipkan. Bisa dikembalikan atau dihapus permanen.</p>
                    </div>
                    <span id="label-total-archivess" class="text-xs font-bold bg-slate-100 text-slate-700 px-3 py-1 rounded-full">0 Arsip</span>
                </div>
                <div id="list-archivess" class="space-y-3"></div>
            </div>
        </div>

    </div>

    <!-- ================= MODALS ================= -->
    <div id="modal-produksi" class="modal-overlay hidden">
        <div class="modal-content">
            <div class="flex justify-between items-center border-b border-slate-200 pb-3 mb-4">
                <h3 class="text-sm font-bold text-indigo-900" id="modal-produksi-title">✏️ Edit Produksi</h3>
                <button onclick="closeModal()" class="text-slate-400 hover:text-slate-600 text-2xl leading-none">&times;</button>
            </div>
            <div id="modal-produksi-body" class="space-y-4"></div>
            <div class="flex justify-end gap-3 mt-5 pt-4 border-t border-slate-200">
                <button onclick="closeModal()" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold px-5 py-2.5 rounded-xl text-sm transition">Tutup</button>
                <button onclick="saveModalProduksi()" class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold px-5 py-2.5 rounded-xl text-sm shadow-lg hover:shadow-indigo-500/30 transition-all hover:scale-[1.02]">💾 Simpan</button>
            </div>
        </div>
    </div>

    <div id="modal-laporan" class="modal-overlay hidden">
        <div class="modal-content" style="max-width: 800px;">
            <div class="flex justify-between items-center border-b border-slate-200 pb-3 mb-4">
                <h3 class="text-sm font-bold text-indigo-900" id="modal-laporan-title">📄 Laporan</h3>
                <button onclick="closeModalLaporan()" class="text-slate-400 hover:text-slate-600 text-2xl leading-none">&times;</button>
            </div>
            <div id="modal-laporan-body" class="laporan-preview"></div>
            <div class="flex justify-end gap-3 mt-5 pt-4 border-t border-slate-200">
                <button onclick="closeModalLaporan()" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold px-5 py-2.5 rounded-xl text-sm transition">Tutup</button>
                <button onclick="downloadModalLaporan()" id="btn-download-laporan" class="bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-bold px-5 py-2.5 rounded-xl text-sm shadow-lg hover:shadow-emerald-500/30 transition-all hover:scale-[1.02]">📥 Download PDF</button>
            </div>
        </div>
    </div>

    <div id="modal-user" class="modal-overlay hidden">
        <div class="modal-content" style="max-width: 600px;">
            <div class="flex justify-between items-center border-b border-slate-200 pb-3 mb-4">
                <h3 class="text-sm font-bold text-indigo-900" id="modal-user-title">➕ Tambah User</h3>
                <button onclick="document.getElementById('modal-user').classList.add('hidden')" class="text-slate-400 hover:text-slate-600 text-2xl leading-none">&times;</button>
            </div>
            <input type="hidden" id="modal-user-id">
            <div class="space-y-4">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-1">Nama Lengkap</label>
                        <input type="text" id="modal-user-nama" placeholder="Nama User" class="w-full border border-slate-200 p-3 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-1">Username</label>
                        <input type="text" id="modal-user-username" placeholder="Username" class="w-full border border-slate-200 p-3 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-1">Password (terlihat jelas untuk admin)</label>
                    <input type="text" id="modal-user-password" placeholder="Password" class="w-full border border-slate-200 p-3 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent font-mono">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-2">Role / Template Hak Akses</label>
                    <select id="modal-user-role" onchange="applyRoleTemplate(this.value)" class="w-full border border-slate-200 p-3 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white">
                        <option value="admin">🔑 Admin (Semua Akses)</option>
                        <option value="marketing">📊 Marketing (SPK & Riwayat)</option>
                        <option value="custom">⚙️ Custom (Atur Manual)</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-2">🗂️ Hak Akses Menu (Centang yang boleh diakses)</label>
                    <div class="access-checkbox-grid" id="access-checkbox-grid">
                        <label><input type="checkbox" class="menu-access" value="spk"> 📋 Input SPK</label>
                        <label><input type="checkbox" class="menu-access" value="harga"> 💰 Master</label>
                        <label><input type="checkbox" class="menu-access" value="history"> 📂 Riwayat SPK</label>
                        <label><input type="checkbox" class="menu-access" value="gudang"> 🏭 Gudang</label>
                        <label><input type="checkbox" class="menu-access" value="produksi"> ⚙️ Produksi</label>
                        <label><input type="checkbox" class="menu-access" value="barangjadi"> 📦 Barang Jadi</label>
                        <label><input type="checkbox" class="menu-access" value="stoksisa"> 📊 Stok Sisa</label>
                        <label><input type="checkbox" class="menu-access" value="archive"> 🗄️ Arsip</label>
                        <label><input type="checkbox" class="menu-access" value="archivebj"> 📦 Arsip BJ</label>
                        <label><input type="checkbox" class="menu-access" value="archivess"> 📊 Arsip SS</label>
                    </div>
                    <p class="text-[10px] text-slate-400 mt-1">💡 Pilih role di atas untuk template, atau centang manual untuk custom</p>
                </div>
            </div>
            <div class="flex justify-end gap-3 mt-5 pt-4 border-t border-slate-200">
                <button onclick="document.getElementById('modal-user').classList.add('hidden')" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold px-5 py-2.5 rounded-xl text-sm transition">Batal</button>
                <button onclick="saveUser()" class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold px-5 py-2.5 rounded-xl text-sm shadow-lg hover:shadow-indigo-500/30 transition-all hover:scale-[1.02]">💾 Simpan</button>
            </div>
        </div>
    </div>

    <div id="pdf-render-area"></div>
"""

with open('part1.html', 'w') as f:
    f.write(html_head_and_body)
print('part1 written successfully')
