<script lang="ts">
    import BirthCertificateTable from "$lib/components/BirthCertificateTable.svelte";
    import { goto } from "$app/navigation";
    
    // 更新ハンドラ
    function handleUpdate(field: string, value: string) {
        console.log(`Updated ${field}: ${value}`);
        // ここにストア更新ロジックを追加可能
    }
    
    // ホームに戻る
    function goHome() {
        goto("/");
    }
</script>

<svelte:head>
    <title>出生証明書（テーブル形式）- 翻訳文書</title>
</svelte:head>

<div class="min-h-screen bg-gray-200 py-6">
    <!-- ナビゲーション -->
    <div class="max-w-[210mm] mx-auto mb-3 flex justify-between items-center px-2">
        <button
            on:click={goHome}
            class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-1.5 px-3 border border-gray-400 rounded shadow text-sm transition-colors"
        >
            ← ホームに戻る
        </button>
        <div class="flex gap-2">
            <a
                href="/birthA4"
                target="_blank"
                class="bg-blue-100 hover:bg-blue-600 hover:text-white text-blue-800 font-semibold py-1.5 px-3 border border-blue-800 rounded shadow text-sm transition-colors"
            >
                A4 バージョン
            </a>
            <button
                onclick="window.print()"
                class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-1.5 px-3 border border-blue-800 rounded shadow text-sm transition-colors"
            >
                📄 印刷
            </button>
        </div>
    </div>

    <!-- テーブル形式証明書コンポーネント -->
    <BirthCertificateTable 
        onUpdate={handleUpdate}
    />
</div>

<style>
    @media print {
        body * {
            visibility: hidden;
        }
        .min-h-screen, .min-h-screen * {
            visibility: visible;
        }
        .min-h-screen {
            position: absolute;
            left: 0;
            top: 0;
            padding: 0 !important;
        }
        button, a {
            display: none !important;
        }
        .bg-gray-200 {
            background: white !important;
            padding: 0 !important;
        }
        .shadow-lg {
            box-shadow: none !important;
        }
    }
</style>
