<script lang="ts">
    import MarriageCertificateTable from "$lib/components/MarriageCertificateTable.svelte";
    import { goto } from "$app/navigation";
    import { marriageStore, updateMarriageData, clearMarriageStore, saveMarriageBackup } from "$lib/stores/marriageStore";

    $: certificateData = $marriageStore;

    function handleUpdate(field: string, value: string) {
        updateMarriageData({ [field]: value });
    }

    function goHome() {
        goto("/");
    }
</script>

<svelte:head>
    <title>婚姻証明書 - 翻訳文書</title>
</svelte:head>

<div class="min-h-screen bg-gray-200 py-6 print:bg-white print:py-0">
    <div class="max-w-[210mm] mx-auto mb-3 flex justify-between items-center px-2 print:hidden">
        <button
            on:click={goHome}
            class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-1.5 px-3 border border-gray-400 rounded shadow text-sm transition-colors"
        >
            ← ホームに戻る
        </button>
        <div class="flex gap-2">
            <button
                on:click={() => { clearMarriageStore(); goto('/'); }}
                class="bg-red-100 hover:bg-red-600 hover:text-white text-red-800 font-semibold py-1.5 px-3 border border-red-800 rounded shadow text-sm transition-colors"
            >
                クリア
            </button>
            <button
                on:click={async () => {
                    const result = await saveMarriageBackup();
                    if (result.success) {
                        alert(`バックアップを保存しました：${result.filename}`);
                    } else {
                        alert(`エラー：${result.error}`);
                    }
                }}
                class="bg-blue-100 hover:bg-blue-600 hover:text-white text-blue-800 font-semibold py-1.5 px-3 border border-blue-800 rounded shadow text-sm transition-colors"
            >
                バックアップ保存
            </button>
            <button
                onclick="window.print()"
                class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-1.5 px-3 border border-blue-800 rounded shadow text-sm transition-colors"
            >
                📄 印刷
            </button>
        </div>
    </div>

    <MarriageCertificateTable
        data={certificateData}
        onUpdate={handleUpdate}
    />
</div>

<style>
    @media print {
        @page {
            margin: 10mm;
            size: A4;
        }

        body {
            margin: 0 !important;
            padding: 0 !important;
            width: 180mm !important;
        }

        body * {
            visibility: hidden;
        }

        .min-h-screen, .min-h-screen * {
            visibility: visible;
        }

        .min-h-screen {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            padding: 0 !important;
            margin: 0 !important;
            width: 180mm !important;
        }

        button, a {
            display: none !important;
        }

        .bg-gray-200 {
            background: white !important;
            padding: 0 !important;
        }

        .shadow-md {
            box-shadow: none !important;
            border: none !important;
        }

        div[class*="max-w"] {
            border: none !important;
            box-shadow: none !important;
        }
    }
</style>
