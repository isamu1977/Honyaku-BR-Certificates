<script lang="ts">
    import BirthCertificateA4 from "$lib/components/BirthCertificateA4.svelte";
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
    <title>出生証明書 - 翻訳文書</title>
</svelte:head>

<div class="min-h-screen bg-gray-200 py-8">
    <!-- ナビゲーション -->
    <div class="max-w-[210mm] mx-auto mb-4 flex justify-between items-center">
        <button
            on:click={goHome}
            class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow transition-colors"
        >
            ← ホームに戻る
        </button>
        <button
            onclick="window.print()"
            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 border border-blue-800 rounded shadow transition-colors"
        >
            📄 印刷
        </button>
    </div>

    <!-- A4 証明書コンポーネント -->
    <BirthCertificateA4 
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
        }
        button {
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
