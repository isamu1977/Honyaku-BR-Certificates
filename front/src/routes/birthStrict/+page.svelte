<script lang="ts">
    import BirthCertificateStrictTable from "$lib/components/BirthCertificateStrictTable.svelte";
    import { goto } from "$app/navigation";
    import { birthStrictStore, updateBirthStrictData, clearBirthStrictStore, saveBirthStrictBackup } from "$lib/stores/birthStrictStore";
    import type { BirthStrictData } from "$lib/types/birthStrict";

    // ストアを購読（Svelte 4 の $ プレフィックス）
    $: certificateData = $birthStrictStore;

    // 更新ハンドラ
    function handleUpdate(field: string, value: string) {
        updateBirthStrictData({ [field]: value });
    }

    // ホームに戻る
    function goHome() {
        goto("/");
    }
</script>

<svelte:head>
    <title>Honyaku BR Certificates - 出生証明書</title>
</svelte:head>

<div class="min-h-screen bg-gray-200 py-6 print:bg-white print:py-0">
    <!-- ナビゲーション -->
    <div class="max-w-[210mm] mx-auto mb-3 flex justify-between items-center px-2 print:hidden">
        <button
            on:click={goHome}
            class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-1.5 px-3 border border-gray-400 rounded shadow text-sm transition-colors"
        >
            ← ホームに戻る
        </button>
        <div class="flex gap-2">
            <button
                on:click={() => { clearBirthStrictStore(); goto('/'); }}
                class="bg-red-100 hover:bg-red-600 hover:text-white text-red-800 font-semibold py-1.5 px-3 border border-red-800 rounded shadow text-sm transition-colors"
            >
                クリア
            </button>
            <button
                on:click={async () => {
                    const result = await saveBirthStrictBackup();
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

    <!-- 厳密テーブル形式証明書コンポーネント -->
    <BirthCertificateStrictTable
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

        /* 外部ボーダーを完全に除去 */
        div[class*="max-w"] {
            border: none !important;
            box-shadow: none !important;
        }
    }
</style>
