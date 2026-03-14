<script>
  import OneLineCell from "$lib/components/OneLineCell.svelte";
  import TwoLinesCellSimple from "$lib/components/TwoLinesCellSimple.svelte";
  import MarryTwoLinesCellCouple from "$lib/components/MarryTwoLinesCellCouple.svelte";
  import MarryTwoLinesCell from "$lib/components/MarryTwoLinesCell.svelte";
  import TranslatorData from "$lib/components/TranslatorData.svelte";
  import EditableField from "$lib/components/EditableField.svelte";
  import { marryCertificationData } from "$lib/data/marryNewVersionData.js";
  import {
    certificationStore,
    saveBackup,
    restoreOriginalData,
  } from "$lib/stores/certificationStore";

  let saveMessage = "";
  let isSaving = false;

  function printDiv() {
    const printContents = document.getElementById("printableDiv").innerHTML;
    const originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;

    window.print();

    document.body.innerHTML = originalContents;
    window.location.reload();
  }

  async function handleSaveBackup() {
    isSaving = true;
    saveMessage = "";
    const result = await saveBackup();
    isSaving = false;
    if (result.success) {
      saveMessage = "バックアップを保存しました！";
      setTimeout(() => (saveMessage = ""), 3000);
    } else {
      saveMessage = "エラー: " + result.error;
    }
  }

  function handleRestore() {
    if (confirm("元のデータに戻しますか？")) {
      restoreOriginalData();
      saveMessage = "元のデータに戻しました";
      setTimeout(() => (saveMessage = ""), 3000);
    }
  }

  function updateField(key, value) {
    certificationStore.update((store) => ({
      ...store,
      [key]: value,
    }));
  }

  $: data = $certificationStore.documentType
    ? $certificationStore
    : marryCertificationData;

  $: titleAditional1 = data.titleAditional1;
  $: titleAditional2 = data.titleAditional2;

  $: husbandSingleName = data.husbandSingleName;
  $: husbandKosekiName = data.husbandKosekiName;
  $: husbandKojinBango = data.husbandKojinBango;

  $: wifeSingleName = data.wifeSingleName;
  $: wifeKosekiName = data.wifeKosekiName;
  $: wifeKojinBango = data.wifeKojinBango;

  $: registrationNum = data.registrationNum;

  $: husbandName = data.husbandName;
  $: husbandBirthDate = data.husbandBirthDate;
  $: husbandBirthPlace = data.husbandBirthPlace;
  $: husbandCitizenship = data.husbandCitizenship;
  $: husbandFatherName = data.husbandFatherName;
  $: husbandFatherKosekiName = data.husbandFatherKosekiName;
  $: husbandMotherName = data.husbandMotherName;
  $: husbandMotherKosekiName = data.husbandMotherKosekiName;

  $: wifeName = data.wifeName;
  $: wifeBirthDate = data.wifeBirthDate;
  $: wifeBirthPlace = data.wifeBirthPlace;
  $: wifeCitizenship = data.wifeCitizenship;
  $: wifeFatherName = data.wifeFatherName;
  $: wifeFatherKosekiName = data.wifeFatherKosekiName;
  $: wifeMotherName = data.wifeMotherName;
  $: wifeMotherKosekiName = data.wifeMotherKosekiName;

  $: registrationDate = data.registrationDate;

  $: marryCondition = data.marryCondition;

  $: husbandMarriedName = data.husbandMarriedName;
  $: wifeMarriedName = data.wifeMarriedName;

  $: registrationChange = data.registrationChange;
  $: registrationAditionalInfo = data.registrationAditionalInfo;

  $: notaryName = data.notaryName;
  $: notaryState = data.notaryState;
  $: scrivenerName = data.scrivenerName;
  $: digitalSignDate1 = data.digitalSignDate1;
  $: digitalSignDate2 = data.digitalSignDate2;
  $: mainScrivenerName = data.mainsScrivenerName;

  $: emissionDate = data.emissionDate;
  $: notaryCity = data.notaryCity;
  $: scrivenerSignCity = data.scrivenerSignCity;
  $: scrivenerSignName = data.scrivenerSignName;
  $: scrivenerType = data.scrivenerType;
  $: scrivenerCity = data.scrivenerCity;

  $: backRegistrationChange = data.backRegistrationChange;
</script>

<div class="flex justify-center gap-2 my-5 flex-wrap">
  <button
    class="
            my-4
            h-14 w-36
            bg-black
            text-xl text-white font-bold
            rounded-lg hover:scale-[1.1]
        "
    on:click={handleSaveBackup}
    disabled={isSaving}
  >
    {isSaving ? "保存中..." : "バックアップ保存"}
  </button>
  <button
    class="
            my-4
            h-14 w-36
            bg-gray-600
            text-xl text-white font-bold
            rounded-lg hover:scale-[1.1]
        "
    on:click={handleRestore}
  >
    元に戻す
  </button>
  <button
    class="
            my-4
            h-14 w-36
            bg-black
            text-2xl text-white font-bold
            rounded-lg hover:scale-[1.1]
        "
    on:click={printDiv}
  >
    印刷
  </button>
</div>

{#if saveMessage}
  <div
    class="text-center mb-4 {saveMessage.includes('エラー')
      ? 'text-red-600'
      : 'text-green-600'} font-semibold"
  >
    {saveMessage}
  </div>
{/if}

<div id="printableDiv" class="flex flex-col items-center">
  <!--Front Page Container Start-->
  <div
    class="
            h-[100vh] w-[213mm]
            flex flex-col
        "
  >
    <div class="border-[2px] border-black p-2 w-full scale-[0.85] -mb-10">
      <div class="w-full mb-3">
        <h1 class="font-bold text-lg text-center italic">ブラジル連邦共和国</h1>
        <h1 class="font-bold text-lg text-center mb-2 italic">
          自然人登記役場
        </h1>

        <div class="flex justify-center items-center">
          <h1 class="font-bold text-4xl italic">結婚証明書</h1>

          {#if titleAditional1}
            <h1 class="font-bold text-4xl">{titleAditional1}</h1>
          {/if}
        </div>

        {#if titleAditional2}
          <h1 class="font-bold text-center">{titleAditional2}</h1>
        {/if}
      </div>

      <div class="">
        {#if husbandKojinBango}
          <MarryTwoLinesCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[69%]"}
            spanTitle={"氏名"}
            firstLineContent1={husbandSingleName}
            firstLineContent2={husbandKosekiName}
            secondLineContent1={wifeSingleName}
            secondLineContent3={wifeKosekiName}
            editable={true}
            onFirstUpdate={(index, v) => {
              if (index === 1) updateField("husbandSingleName", v);
              else if (index === 2) updateField("husbandKosekiName", v);
              else if (index === 3) updateField("wifeSingleName", v);
              else if (index === 4) updateField("wifeKosekiName", v);
            }}
            onSecondUpdate={(index, v) => {
              if (index === 1) updateField("wifeSingleName", v);
              else if (index === 2) updateField("wifeKosekiName", v);
            }}
          />
        {/if}

        {#if !husbandKojinBango}
          <MarryTwoLinesCell
            divStyle={"text-center pl-3 pt-1 inline-block relative w-[99%]"}
            spanTitle={"氏名"}
            firstLineContent1={husbandSingleName}
            firstLineContent2={husbandKosekiName}
            secondLineContent1={wifeSingleName}
            secondLineContent3={wifeKosekiName}
            editable={true}
            onFirstUpdate={(index, v) => {
              if (index === 1) updateField("husbandSingleName", v);
              else if (index === 2) updateField("husbandKosekiName", v);
              else if (index === 3) updateField("wifeSingleName", v);
              else if (index === 4) updateField("wifeKosekiName", v);
            }}
            onSecondUpdate={(index, v) => {
              if (index === 1) updateField("wifeSingleName", v);
              else if (index === 2) updateField("wifeKosekiName", v);
            }}
          />
        {/if}

        {#if husbandKojinBango}
          <MarryTwoLinesCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[30%]"}
            spanTitle={"個人納税者番号"}
            firstLineContent1={husbandKojinBango}
            firstLineContent2={""}
            secondLineContent1={wifeKojinBango}
            secondLineContent3={""}
            editable={true}
            onFirstUpdate={(index, v) => {
              if (index === 1) updateField("husbandKojinBango", v);
              else if (index === 3) updateField("wifeKojinBango", v);
            }}
            onSecondUpdate={(index, v) => {
              if (index === 1) updateField("husbandKojinBango", v);
              else if (index === 3) updateField("wifeKojinBango", v);
            }}
          />
        {/if}
      </div>

      <div class="w-full mb-5">
        <h1 class="font-semibold text-center">登録番号</h1>
        <h1 class="font-bold text-2xl text-center min-h-6">
          <EditableField
            value={registrationNum}
            onChange={(v) => updateField("registrationNum", v)}
          />
        </h1>
      </div>

      <div class="w-full">
        <div class="w-full mb-5">
          <MarryTwoLinesCellCouple
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
            spanTitle={"新郎新婦情報"}
            firstLineTitle={"夫"}
            firstLineContent1={husbandName}
            firstLineContent2={husbandBirthDate}
            firstLineContent3={husbandBirthPlace}
            firstLineContent4={husbandCitizenship}
            firstLineContent5={husbandFatherName}
            firstLineContent6={husbandFatherKosekiName}
            firstLineContent7={husbandMotherName}
            secondLineTitle={"妻"}
            secondLineContent1={wifeName}
            secondLineContent2={wifeBirthDate}
            secondLineContent3={wifeBirthPlace}
            secondLineContent4={wifeCitizenship}
            secondLineContent5={wifeFatherName}
            secondLineContent6={wifeFatherKosekiName}
            secondLineContent7={wifeMotherName}
            editable={true}
            onFirstUpdate={(index, v) => {
              if (index === 1) updateField("husbandName", v);
              else if (index === 2) updateField("husbandBirthDate", v);
              else if (index === 3) updateField("husbandBirthPlace", v);
              else if (index === 4) updateField("husbandCitizenship", v);
              else if (index === 5) updateField("husbandFatherName", v);
              else if (index === 6) updateField("husbandFatherKosekiName", v);
              else if (index === 7) updateField("husbandMotherName", v);
            }}
            onSecondUpdate={(index, v) => {
              if (index === 1) updateField("wifeName", v);
              else if (index === 2) updateField("wifeBirthDate", v);
              else if (index === 3) updateField("wifeBirthPlace", v);
              else if (index === 4) updateField("wifeCitizenship", v);
              else if (index === 5) updateField("wifeFatherName", v);
              else if (index === 6) updateField("wifeFatherKosekiName", v);
              else if (index === 7) updateField("wifeMotherName", v);
            }}
          />
        </div>

        <div class="w-full mb-5">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
            spanTitle={"婚姻登録日"}
            pContent={registrationDate}
            editable={true}
            onUpdate={(v) => updateField("registrationDate", v)}
          />
        </div>

        <div class="w-full mb-5">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
            spanTitle={"婚姻条件"}
            pContent={marryCondition}
            editable={true}
            onUpdate={(v) => updateField("marryCondition", v)}
          />
        </div>

        <div class="mt-4 w-full mb-5">
          <TwoLinesCellSimple
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
            spanTitle={"婚姻後の改姓"}
            firstLineTitle={"夫"}
            firstLineContent1={husbandMarriedName}
            secondLineTitle={"妻"}
            secondLineContent1={wifeMarriedName}
            editable={true}
            onUpdate1={(v) => updateField("husbandMarriedName", v)}
            onUpdate2={(v) => updateField("wifeMarriedName", v)}
          />
        </div>

        <div class="mt-4 w-full mb-5">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99.5%]"}
            spanTitle={"変更・追記"}
            pContent={registrationChange}
            editable={true}
            onUpdate={(v) => updateField("registrationChange", v)}
          />
        </div>

        <div class="mt-4 w-full mb-3">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99.5%]"}
            spanTitle={"備考・記録"}
            pContent={registrationAditionalInfo}
            editable={true}
            onUpdate={(v) => updateField("registrationAditionalInfo", v)}
          />
        </div>

        <div class="w-full mb-5">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
            spanTitle={"婚姻登録日"}
            pContent={registrationDate}
          />
        </div>

        <div class="w-full mb-5">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
            spanTitle={"婚姻条件"}
            pContent={marryCondition}
          />
        </div>

        <div class="mt-4 w-full mb-5">
          <TwoLinesCellSimple
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
            spanTitle={"婚姻後の改姓"}
            firstLineTitle={"夫"}
            firstLineContent1={husbandMarriedName}
            secondLineTitle={"妻"}
            secondLineContent1={wifeMarriedName}
          />
        </div>

        <div class="mt-4 w-full mb-5">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99.5%]"}
            spanTitle={"変更・追記"}
            pContent={registrationChange}
          />
        </div>

        <div class="mt-4 w-full mb-3">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99.5%]"}
            spanTitle={"備考・記録"}
            pContent={registrationAditionalInfo}
          />
        </div>
      </div>
      {#if digitalSignDate1}
        <div class="w-full mt-2">
          <p class="mb-2">
            <EditableField
              value={digitalSignDate1}
              onChange={(v) => updateField("digitalSignDate1", v)}
            />
            に民事登録情報センターの情報に基づき、当証明書を作成し、電子署名を確認しました。
          </p>
          <p class="">
            <EditableField
              value={notaryName}
              onChange={(v) => updateField("notaryName", v)}
            />
            、
            <EditableField
              value={scrivenerName}
              onChange={(v) => updateField("scrivenerName", v)}
            />
            が
            <EditableField
              value={digitalSignDate2}
              onChange={(v) => updateField("digitalSignDate2", v)}
            />
            に作成し、電子署名しました。
          </p>
        </div>
      {/if}

      <div class="flex w-full my-5">
        <div class="w-[50%] text-center">
          <p class="">
            <EditableField
              value={notaryName}
              onChange={(v) => updateField("notaryName", v)}
            />
          </p>
          <p class="my-2">
            <EditableField
              value={mainScrivenerName}
              onChange={(v) => updateField("mainsScrivenerName", v)}
            />
            公証人
          </p>
          <p class="">
            <EditableField
              value={notaryCity}
              onChange={(v) => updateField("notaryCity", v)}
            />
            <EditableField
              value={notaryState}
              onChange={(v) => updateField("notaryState", v)}
            />
          </p>
        </div>

        <div class="w-[50%] text-center">
          <p class="">以上事実である事を証明致します。</p>
          {#if !emissionDate}
            <div class="h-6"></div>
          {/if}
          {#if emissionDate}
            <p class="my-3">
              <EditableField
                value={notaryCity}
                onChange={(v) => updateField("notaryCity", v)}
              />
              、
              <EditableField
                value={emissionDate}
                onChange={(v) => updateField("emissionDate", v)}
              />
            </p>
          {/if}
          <p class="border-b-[1px] border-black">
            <EditableField
              value={scrivenerSignName}
              onChange={(v) => updateField("scrivenerSignName", v)}
            />
          </p>
          <p class="">
            <EditableField
              value={scrivenerType}
              onChange={(v) => updateField("scrivenerType", v)}
            />
          </p>
          {#if scrivenerCity}
            <p class="">
              <EditableField
                value={scrivenerCity}
                onChange={(v) => updateField("scrivenerCity", v)}
              />
            </p>
          {/if}
        </div>
      </div>
    </div>

    <div class="scale-[0.85]">
      <TranslatorData />
    </div>
  </div>
  <!--Front Page Container End-->

  {#if backRegistrationChange}
    <!--Back Page Container Start-->
    <div
      class="
            page-break
            w-[213mm] min-h-[100vh]
            flex flex-col
            "
    >
      <div class="mt-16 scale-[0.85]">
        <div class="w-full">
          <OneLineCell
            divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99.5%]"}
            spanTitle={"変更・追記"}
            pContent={backRegistrationChange}
          />
        </div>

        <div class="flex w-full my-4">
          <div class="w-[50%] text-center">
            <p class="">{notaryName}</p>
            <p class="my-2">{mainScrivenerName}公証人</p>
            <p class="">{notaryCity} {notaryState}</p>
          </div>

          <div class="w-[50%] text-center">
            <p class="">以上事実である事を証明致します。</p>
            {#if !emissionDate}
              <div class="h-6"></div>
            {/if}
            {#if emissionDate}
              <p class="my-3">{notaryCity}、{emissionDate}</p>
            {/if}
            <p class="border-b-[1px] border-black">{scrivenerSignName}</p>
            <p class="">{scrivenerType}</p>
            {#if scrivenerCity}
              <p class="">{scrivenerCity}</p>
            {/if}
          </div>
        </div>
        <div class="-mt-12">
          <TranslatorData />
        </div>
      </div>
    </div>
    <!--Back Page Container End-->
  {/if}
</div>

<style>
  @media print {
    .page-break {
      page-break-before: always;
    }
    #printableDiv {
      display: block;
      align-items: normal;
      justify-content: normal;
    }
  }
</style>
