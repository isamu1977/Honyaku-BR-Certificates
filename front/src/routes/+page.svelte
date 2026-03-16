<script lang="ts">
  import { goto } from "$app/navigation";
  import { updateCertificationData } from "$lib/stores/certificationStore";
  import { setBirthStrictData } from "$lib/stores/birthStrictStore";
  import { setMarriageData } from "$lib/stores/marriageStore";
  import { onMount } from "svelte";
  import ProviderSelector from "$lib/components/ProviderSelector.svelte";

  // バックエンド URL を環境変数から取得（デフォルト：http://localhost:8080）
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8080";

  let showButton = false;
  let isLoading = false;
  let errorMessage = "";
  let fileInput;
  let backups = [];
  let isLoadingBackups = false;
  let selectedProvider = "ollama";
  let selectedModel = "qwen3.5:2b";
  let selectedFile = null;
  let previewUrl = null;
  let isBackendOnline = false;

  function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    selectedFile = file;
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    previewUrl = URL.createObjectURL(file);
    errorMessage = "";
  }

  async function startTranslation(docType) {
    if (!selectedFile) {
      errorMessage = "Por favor, selecione uma imagem primeiro.";
      return;
    }

    isLoading = true;
    errorMessage = "";

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("provider", selectedProvider);
    formData.append("model", selectedModel);
    formData.append("document_type", docType);

    try {
      const response = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Upload failed");
      }

      const data = await response.json();
      console.log("Response from backend:", data);

      if (data.error) {
        throw new Error(data.error);
      }

      // BIRTH_STRICT の場合は新しいストアを使用
      if (docType === "BIRTH_STRICT") {
        setBirthStrictData(data);
        goto("/birthStrict");
      } else if (docType === "MARRIAGE_STRICT") {
        setMarriageData(data);
        goto("/marriage");
      } else {
        updateCertificationData(data);
        // 他のドキュメントタイプの場合は既存のルーティング
        if (docType === "MARRIAGE_NEW_VER1" || docType === "MARRIAGE_NEW_VER2" || docType === "MARRIAGE_OLD") {
          goto("/marryNewVersion");
        } else if (docType === "BIRTH_NEW_VER1" || docType === "BIRTH_NEW_VER2") {
          goto("/birthNewVersion");
        } else if (docType === "BIRTH_OLD") {
          goto("/birthOldVersion");
        }
      }
    } catch (error) {
      console.error("Error processing file:", error);
      errorMessage = "エラーが発生しました: " + error.message;
    } finally {
      isLoading = false;
    }
  }

  async function loadBackups() {
    isLoadingBackups = true;
    try {
      const response = await fetch(`${BACKEND_URL}/backups`);
      if (response.ok) {
        backups = await response.json();
      }
    } catch (error) {
      console.error("Error loading backups:", error);
    } finally {
      isLoadingBackups = false;
    }
  }

  async function loadBackup(filename) {
    try {
      const response = await fetch(`${BACKEND_URL}/backup/${filename}`);
      if (response.ok) {
        const data = await response.json();
        
        const docType = data.documentType
          ? data.documentType.toUpperCase()
          : "";

        if (docType === "BIRTH_STRICT") {
          setBirthStrictData(data);
          goto("/birthStrict");
        } else if (docType === "MARRIAGE_STRICT") {
          setMarriageData(data);
          goto("/marriage");
        } else if (docType === "MARRIAGE_NEW" || docType === "MARRIAGE_OLD") {
          goto("/marryNewVersion");
        } else if (docType === "BIRTH_NEW") {
          goto("/birthNewVersion");
        } else if (docType === "BIRTH_OLD") {
          goto("/birthOldVersion");
        } else {
          updateCertificationData(data);
          goto("/birthNewVersion");
        }
      }
    } catch (error) {
      console.error("Error loading backup:", error);
      alert("バックアップの読み込み中にエラーが発生しました");
    }
  }

  async function deleteBackup(filename) {
    if (!confirm("このバックアップを削除しますか？")) return;

    try {
      const response = await fetch(`${BACKEND_URL}/backup/${filename}`, {
        method: "DELETE",
      });
      if (response.ok) {
        await loadBackups();
      }
    } catch (error) {
      console.error("Error deleting backup:", error);
      alert("バックアップの削除中にエラーが発生しました");
    }
  }

  function getDocumentTypeLabel(docType) {
    switch (docType) {
      case "BIRTH_NEW":
        return "出生証明書（新）";
      case "BIRTH_OLD":
        return "出生証明書（旧）";
      case "MARRIAGE_NEW":
        return "結婚証明書（新）";
      default:
        return docType;
    }
  }

  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString("ja-JP");
  }

  async function toggleBackend() {
    try {
      const action = isBackendOnline ? "stop" : "start";
      const response = await fetch(`${BACKEND_URL}/api/start-backend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || data.error || "Failed to toggle backend");

      if (action === "start") {
        alert(`バックエンドを起動しました：${data.message}`);
        isBackendOnline = true;
      } else {
        alert(`バックエンドを停止しました：${data.message}`);
        isBackendOnline = false;
      }
    } catch (e: any) {
      alert("エラー：" + e.message);
    }
  }

  onMount(() => {
    loadBackups();

    // Initial backend check
    fetch(`${BACKEND_URL}/`).then(r => isBackendOnline = r.ok).catch(() => isBackendOnline = false);

    // Poll backend status
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${BACKEND_URL}/`);
        isBackendOnline = res.ok;
      } catch (e) {
        isBackendOnline = false;
      }
    }, 3000);

    return () => clearInterval(interval);
  });
</script>

<svelte:head>
  <title>Honyaku BR Certificates</title>
</svelte:head>

<main
  class="flex flex-col min-h-screen w-full bg-[#f4f4f0] text-black font-sans selection:bg-black selection:text-white p-4 md:p-12"
>
  <header
    class="w-full flex justify-between items-end border-b-2 border-black pb-4 mb-12"
  >
    <h1
      class="font-mono text-4xl md:text-6xl font-black uppercase tracking-tighter leading-none"
    >
      Honyaku BR<br /><span class="text-xl md:text-3xl font-light tracking-widest"
        >Certificates</span
      >
    </h1>
    <div
      class="text-right flex flex-col items-end font-mono text-xs uppercase tracking-widest gap-2"
    >
      <div>
        <p>
          System Status: <span class={isBackendOnline ? "text-green-600 font-bold" : "text-red-600 font-bold"}>• {isBackendOnline ? 'ONLINE' : 'OFFLINE'}</span>
        </p>
        <p>Mode: <span class="font-bold">PRODUCTION</span></p>
      </div>
      <div class="flex gap-2 flex-wrap justify-end">
        <button
          on:click={toggleBackend}
          class="border-2 border-black px-3 py-1.5 font-bold text-xs bg-yellow-300 hover:bg-yellow-400 transition-colors shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] hover:shadow-[1px_1px_0px_0px_rgba(0,0,0,1)] hover:translate-x-[1px] hover:translate-y-[1px]"
        >
          {#if isBackendOnline}
            [ 🛑 STOP BACKEND ]
          {:else}
            [ ▶️ START BACKEND ]
          {/if}
        </button>
        <a
          href="/birthStrict"
          target="_blank"
          class="border border-black px-2 py-1 font-bold text-[10px] bg-green-100 hover:bg-green-600 hover:text-white transition-colors"
        >
          [ 厳密テーブル ]
        </a>
        <a
          href="/marriage"
          target="_blank"
          class="border border-black px-2 py-1 font-bold text-[10px] bg-pink-100 hover:bg-pink-600 hover:text-white transition-colors"
        >
          [ 婚姻証明書 ]
        </a>
      </div>
    </div>
  </header>

  <div
    class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-[1600px] mx-auto"
  >
    <!-- Upload and Preview Section -->
    <section
      class="flex flex-col border-2 border-black bg-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] relative overflow-hidden"
    >
      <div
        class="bg-black text-white px-4 py-2 flex justify-between items-center font-mono text-xs font-bold uppercase tracking-widest"
      >
        <span>01 // Input Pipeline</span>
        <span class="animate-pulse">Awaiting Payload</span>
      </div>

      <div class="p-8 md:p-12 flex flex-col h-full">
        <ProviderSelector bind:selectedProvider bind:selectedModel />

        <div
          class="mt-8 w-full flex flex-col items-center justify-center border-2 border-dashed border-black p-12 bg-[#fafafa] hover:bg-black hover:text-white transition-all duration-300 cursor-pointer group"
          on:click={() => fileInput.click()}
          on:keydown={(e) => e.key === "Enter" && fileInput.click()}
          role="button"
          tabindex="0"
        >
            <input
            type="file"
            accept="image/*,application/pdf"
            class="hidden"
            bind:this={fileInput}
            on:change={handleFileSelect}
          />

          {#if previewUrl}
            <div class="relative w-full aspect-[3/4] max-h-[600px] bg-gray-100 flex items-center justify-center overflow-hidden border border-black">
              <img src={previewUrl} alt="Preview" class="object-contain w-full h-full" />
              <button 
                class="absolute top-2 right-2 bg-black text-white px-3 py-1 text-xs font-mono hover:bg-red-600 transition-colors"
                on:click|stopPropagation={() => {
                  selectedFile = null;
                  URL.revokeObjectURL(previewUrl);
                  previewUrl = null;
                  if (fileInput) fileInput.value = '';
                }}
              >
                [REMOVE]
              </button>
            </div>
          {:else}
            <div
              class="text-center group-hover:scale-105 transition-transform duration-300"
            >
              <span class="block text-4xl mb-4 font-light">↓</span>
              <p
                class="font-mono font-bold text-xl uppercase tracking-widest mb-2"
              >
                Inject File Here
              </p>
              <p class="font-mono text-xs uppercase opacity-70">
                Supports JPG, PNG, PDF
              </p>
            </div>
          {/if}
        </div>

        {#if errorMessage}
          <div
            class="mt-6 p-4 border-l-4 border-red-600 bg-red-50 text-red-900 font-mono text-sm uppercase font-bold"
          >
            [ERROR] {errorMessage}
          </div>
        {/if}
      </div>
    </section>

    <!-- Manual Document Types & Backups -->
    <section class="flex flex-col space-y-8">
      <!-- Translation Triggers -->
      <div
        class="border-2 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] relative"
      >
        {#if isLoading}
          <div class="absolute inset-0 z-10 bg-white/80 backdrop-blur-sm flex flex-col items-center justify-center border-t-2 border-black">
            <div class="w-12 h-12 border-4 border-black border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="font-mono font-bold uppercase tracking-widest text-lg animate-pulse">
              Translating...
            </p>
          </div>
        {/if}
        <div
          class="bg-black text-white px-4 py-2 font-mono text-xs font-bold uppercase tracking-widest"
        >
          <span>02 // Translation Engine</span>
        </div>

        <div class="p-6">
          <h2
            class="font-bold text-lg uppercase tracking-wide border-b border-gray-300 pb-2 mb-4"
          >
            Birth Certificate
          </h2>
          <div class="mb-8">
            <button
              class="w-full px-4 py-4 border-2 border-black text-sm font-mono uppercase bg-[#f4f4f0] hover:bg-green-600 hover:text-white hover:border-green-600 transition-colors font-bold tracking-wider"
              on:click={() => startTranslation('BIRTH_STRICT')}
              disabled={isLoading}>
              [ START TRANSLATION ]
            </button>
          </div>

          <h2
            class="font-bold text-lg uppercase tracking-wide border-b border-gray-300 pb-2 mb-4"
          >
            Marriage Cert
          </h2>
          <div class="mb-8">
            <button
              class="w-full px-4 py-4 border-2 border-black text-sm font-mono uppercase bg-[#f4f4f0] hover:bg-green-600 hover:text-white hover:border-green-600 transition-colors font-bold tracking-wider"
              on:click={() => startTranslation('MARRIAGE_STRICT')}
              disabled={isLoading}>
              [ START TRANSLATION ]
            </button>
          </div>
        </div>
      </div>

      <!-- Database / Backups -->
      <div
        class="border-2 border-black bg-white shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] flex-grow flex flex-col"
      >
        <div
          class="bg-black text-white px-4 py-2 flex justify-between items-center font-mono text-xs font-bold uppercase tracking-widest"
        >
          <span>03 // Data Archive</span>
          <button
            class="hover:text-green-400 transition-colors"
            on:click={loadBackups}>[ Refresh ]</button
          >
        </div>

        <div class="p-6 flex-grow overflow-y-auto max-h-[400px]">
          {#if isLoadingBackups}
            <div class="flex items-center justify-center space-x-2 py-8">
              <span class="w-2 h-6 bg-black animate-ping"></span>
              <span class="font-mono text-xs uppercase font-bold"
                >Fetching...</span
              >
            </div>
          {:else if backups.length === 0}
            <p class="font-mono text-xs text-center py-8 opacity-50 uppercase">
              Archive Empty
            </p>
          {:else}
            <div class="flex flex-col space-y-2">
              {#each backups as backup}
                <div
                  class="group flex flex-col border border-black p-3 hover:bg-black hover:text-white transition-colors"
                >
                  <button
                    class="text-left w-full mb-2"
                    on:click={() => loadBackup(backup.filename)}
                  >
                    <div class="font-bold text-sm uppercase truncate mb-1">
                      {backup.name || "UNNAMED_RECORD"}
                    </div>
                    <div
                      class="font-mono text-[10px] opacity-70 flex justify-between"
                    >
                      <span
                        >TYPE:{getDocumentTypeLabel(backup.documentType)}</span
                      >
                      <span>{backup.date && formatDate(backup.modifiedAt)}</span
                      >
                    </div>
                  </button>
                  <div
                    class="flex justify-end border-t border-dashed border-gray-300 group-hover:border-gray-700 pt-2 mt-auto"
                  >
                    <button
                      class="font-mono text-[10px] text-red-600 group-hover:text-red-400 uppercase tracking-widest hover:underline"
                      on:click={() => deleteBackup(backup.filename)}
                    >
                      [ purge ]
                    </button>
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      </div>
    </section>
  </div>
</main>
