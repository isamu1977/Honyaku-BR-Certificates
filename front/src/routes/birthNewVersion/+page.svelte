<script>
    import OneLineCell from "$lib/components/OneLineCell.svelte";
    import TwoLinesCell from "$lib/components/TwoLinesCell.svelte";
    import TwoLinesCellGrand from "$lib/components/TwoLinesCellGrand.svelte";
    import TranslatorData from "$lib/components/TranslatorData.svelte";
    import EditableField from "$lib/components/EditableField.svelte";
    import { birthCertificationData } from "$lib/data/birthNewVersionData.js";
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
        : birthCertificationData;

    $: titleAditional1 = data.titleAditional1;
    $: titleAditional2 = data.titleAditional2;
    $: name = data.name;
    $: kosekiName = data.kosekiName;
    $: kojinNozeishaBango = data.kojinNozeishaBango;
    $: registrationNun = data.registrationNum;
    $: birthDate = data.birthDate;
    $: birthTime = data.birthTime;
    $: birthCityState = data.birthCityState;
    $: registrationPlace = data.registrationPlace;
    $: birthPlace = data.birthPlace;
    $: gender = data.gender;

    $: fatherName = data.fatherName;
    $: fatherKosekiName = data.fatherKosekiName;
    $: fatherBirthPlace = data.fatherBirthPlace;
    $: motherName = data.motherName;
    $: motherKosekiName = data.motherKosekiName;
    $: motherBirthPlace = data.motherBirthPlace;
    $: fatherSideGrandFather = data.fatherSideGrandFather;
    $: fatherSideGrandFatherKosekiName = data.fatherSideGrandFatherKosekiName;
    $: fatherSideGrandMother = data.fatherSideGrandMother;
    $: fatherSideGrandMotherKosekiName = data.fatherSideGrandMotherKosekiName;
    $: motherSideGrandFather = data.motherSideGrandFather;
    $: motherSideGrandFatherKosekiName = data.motherSideGrandFatherKosekiName;
    $: motherSideGrandMother = data.motherSideGrandMother;
    $: motherSideGrandMotherKosekiname = data.motherSideGrandMotherKosekiname;
    $: twins = data.twins;
    $: twinBrotherName = data.twinBrotherName;
    $: registrationDate = data.registrationDate;

    $: newBornNumber = data.newBornNumber;
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
                <h1 class="font-bold text-lg text-center italic">
                    ブラジル連邦共和国
                </h1>
                <h1 class="font-bold text-lg text-center mb-2 italic">
                    自然人登記役場
                </h1>

                <div class="flex justify-center items-center">
                    <h1 class="font-bold text-4xl italic">出生証明書</h1>

                    {#if titleAditional1}
                        <h1 class="font-bold text-4xl">{titleAditional1}</h1>
                    {/if}
                </div>

                {#if titleAditional2}
                    <h1 class="font-bold text-center">{titleAditional2}</h1>
                {/if}
            </div>

            <div class="w-full mb-3">
                <h1 class="font-bold text-center">氏名</h1>
                <h1 class="font-bold text-3xl my-4 text-center">
                    <EditableField
                        value={name}
                        onChange={(v) => updateField("name", v)}
                    />
                </h1>

                {#if kosekiName}
                    <h1 class="font-bold text-2xl text-center">
                        <EditableField
                            value={kosekiName}
                            onChange={(v) => updateField("kosekiName", v)}
                        />
                    </h1>
                {/if}
            </div>

            <div
                class="border border-black pl-3 pt-1 inline-block relative w-full mb-3"
            >
                <span
                    class="absolute -top-3 bg-white px-2 text-sm font-semibold"
                    >個人納税者番号</span
                >
                <EditableField
                    value={kojinNozeishaBango}
                    onChange={(v) => updateField("kojinNozeishaBango", v)}
                />
            </div>

            <div class="w-full mb-5">
                <h1 class="font-semibold text-center">登録番号</h1>
                <h1 class="font-bold text-2xl text-center min-h-6">
                    <EditableField
                        value={registrationNun}
                        onChange={(v) => updateField("registrationNum", v)}
                    />
                </h1>
            </div>

            <div class="w-full">
                <div class="w-full mb-5">
                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[25%]"}
                        spanTitle={"生年月日"}
                        pContent={birthDate}
                        editable={true}
                        onUpdate={(v) => updateField("birthDate", v)}
                    />

                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[23%]"}
                        spanTitle={"出生時間"}
                        pContent={birthTime}
                        editable={true}
                        onUpdate={(v) => updateField("birthTime", v)}
                    />

                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[50%]"}
                        spanTitle={"出生市・州"}
                        pContent={birthCityState}
                        editable={true}
                        onUpdate={(v) => updateField("birthCityState", v)}
                    />
                </div>

                <div class="w-full mb-5">
                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[43%]"}
                        spanTitle={"登録場所"}
                        pContent={registrationPlace}
                        editable={true}
                        onUpdate={(v) => updateField("registrationPlace", v)}
                    />

                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[43%]"}
                        spanTitle={"出生場所"}
                        pContent={birthPlace}
                        editable={true}
                        onUpdate={(v) => updateField("birthPlace", v)}
                    />

                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[12%]"}
                        spanTitle={"性別"}
                        pContent={gender}
                        editable={true}
                        onUpdate={(v) => updateField("gender", v)}
                    />
                </div>

                <div class="mt-4 w-full mb-5">
                    <TwoLinesCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
                        spanTitle={"両親"}
                        firstLineTitle={"父親"}
                        firstLineContent1={fatherName}
                        firstLineContent2={fatherKosekiName}
                        firstLineContent3={fatherBirthPlace}
                        secondLineTitle={"母親"}
                        secondLineContent1={motherName}
                        secondLineContent2={motherKosekiName}
                        secondLineContent3={motherBirthPlace}
                        editable={true}
                        onUpdate1={(v) => updateField("fatherName", v)}
                        onUpdate2={(v) => updateField("fatherKosekiName", v)}
                        onUpdate3={(v) => updateField("fatherBirthPlace", v)}
                        onUpdate4={(v) => updateField("motherName", v)}
                        onUpdate5={(v) => updateField("motherKosekiName", v)}
                        onUpdate6={(v) => updateField("motherBirthPlace", v)}
                    />
                </div>

                <div class="mt-4 w-full mb-5">
                    <TwoLinesCellGrand
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[99%]"}
                        spanTitle={"祖父母"}
                        firstLineTitle={"父親方"}
                        firstLineContent1={fatherSideGrandFather}
                        firstLineContent2={fatherSideGrandFatherKosekiName}
                        firstLineContent3={fatherSideGrandMother}
                        firstLineContent4={fatherSideGrandMotherKosekiName}
                        secondLineTitle={"母親方"}
                        secondLineContent1={motherSideGrandFather}
                        secondLineContent2={motherSideGrandFatherKosekiName}
                        secondLineContent3={motherSideGrandMother}
                        secondLineContent4={motherSideGrandMotherKosekiname}
                        editable={true}
                        onUpdate1={(v) =>
                            updateField("fatherSideGrandFather", v)}
                        onUpdate2={(v) =>
                            updateField("fatherSideGrandFatherKosekiName", v)}
                        onUpdate3={(v) =>
                            updateField("fatherSideGrandMother", v)}
                        onUpdate4={(v) =>
                            updateField("fatherSideGrandMotherKosekiName", v)}
                        onUpdate5={(v) =>
                            updateField("motherSideGrandFather", v)}
                        onUpdate6={(v) =>
                            updateField("motherSideGrandFatherKosekiName", v)}
                        onUpdate7={(v) =>
                            updateField("motherSideGrandMother", v)}
                        onUpdate8={(v) =>
                            updateField("motherSideGrandMotherKosekiname", v)}
                    />
                </div>

                <div class="mt-4 w-full mb-5">
                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[25%]"}
                        spanTitle={"双子の有無"}
                        pContent={twins}
                        editable={true}
                        onUpdate={(v) => updateField("twins", v)}
                    />

                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[74%]"}
                        spanTitle={"双子の氏名・登録"}
                        pContent={twinBrotherName}
                        editable={true}
                        onUpdate={(v) => updateField("twinBrotherName", v)}
                    />
                </div>

                <div class="mt-4 w-full mb-5">
                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[52%]"}
                        spanTitle={"届出年月日"}
                        pContent={registrationDate}
                        editable={true}
                        onUpdate={(v) => updateField("registrationDate", v)}
                    />

                    <OneLineCell
                        divStyle={"border border-black pl-3 pt-1 inline-block relative w-[47%]"}
                        spanTitle={"新生児登録"}
                        pContent={newBornNumber}
                        editable={true}
                        onUpdate={(v) => updateField("newBornNumber", v)}
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
                        onUpdate={(v) =>
                            updateField("registrationAditionalInfo", v)}
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
                            onChange={(v) =>
                                updateField("mainsScrivenerName", v)}
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
                            onChange={(v) =>
                                updateField("scrivenerSignName", v)}
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
                                onChange={(v) =>
                                    updateField("scrivenerCity", v)}
                            />
                        </p>
                    {/if}
                </div>
            </div>
        </div>
        <div class="my-auto scale-[0.85]">
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
                        editable={true}
                        onUpdate={(v) =>
                            updateField("backRegistrationChange", v)}
                    />
                </div>

                <div class="flex w-full my-4">
                    <div class="w-[50%] text-center">
                        <p class="">{notaryName}</p>
                        <p class="my-2">{mainScrivenerName}　公証人</p>
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
                        <p class="border-b-[1px] border-black">
                            {scrivenerSignName}
                        </p>
                        <p class="">{scrivenerType}</p>
                        {#if scrivenerCity}
                            <p class="">{scrivenerCity}</p>
                        {/if}
                    </div>
                </div>
                <div class="">
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
