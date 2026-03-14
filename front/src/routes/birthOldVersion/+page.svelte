<script>
    import OneLineCell from "$lib/components/OneLineCell.svelte";
    import TwoLinesCell from "$lib/components/TwoLinesCell.svelte";
    import TwoLinesCellGrand from "$lib/components/TwoLinesCellGrand.svelte";
    import TranslatorData from "$lib/components/TranslatorData.svelte";
    import EditableField from "$lib/components/EditableField.svelte";
    import { birthCertificationData } from "$lib/data/birthOldVersionData.js";
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

    $: notaryCity = data.notaryCity;
    $: notaryState = data.notaryState;

    $: notaryName = data.notaryName;

    $: titleAditional1 = data.titleAditional1;
    $: titleAditional2 = data.titleAditional2;

    $: mainsScrivenerName = data.mainsScrivenerName;

    $: name = data.name;
    $: kosekiName = data.kosekiName;
    $: gender = data.gender;
    $: birthDate = data.birthDate;
    $: birthTime = data.birthTime;
    $: birthPlace = data.birthPlace;
    $: registrationNun = data.registrationNum;
    $: newBornNumber = data.newBornNumber;

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

    $: registrationDay = data.registrationDate || data.registrationDay;
    $: registrationPerson = data.registrationPerson;
    $: otherRegistration = data.otherRegistration;

    $: registrationAditionalInfo = data.registrationAditionalInfo;

    $: emissionDate = data.emissionDate;
    $: scrivenerSignName = data.scrivenerSignName;
    $: scrivenerType = data.scrivenerType;

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
            min-h-[100vh] w-[213mm]
            flex flex-col
        "
    >
        <div class=" px-8 mb-2 w-full scale-[0.85]">
            <div class="w-full mb-3">
                <h1 class="font-bold text-4xl text-center italic">
                    <EditableField
                        value={notaryCity}
                        onChange={(v) => updateField("notaryCity", v)}
                    />
                </h1>

                <h1 class="font-bold text-2xl text-center italic">
                    <EditableField
                        value={notaryState}
                        onChange={(v) => updateField("notaryState", v)}
                    />
                </h1>

                <h1 class="font-bold text-2xl text-center mb-2 italic">
                    <EditableField
                        value={notaryName}
                        onChange={(v) => updateField("notaryName", v)}
                    />
                    自然人登記役場
                </h1>

                <div class="text-center my-5">
                    <h1 class="font-bold text-xl text-center italic mr-4">
                        <EditableField
                            value={mainsScrivenerName}
                            onChange={(v) =>
                                updateField("mainsScrivenerName", v)}
                        />
                    </h1>
                    <h1 class="font-bold text-lg text-center italic">公証人</h1>
                </div>

                <div class="flex justify-center items-center my-12">
                    <h1 class="font-bold text-4xl italic">出生証明書</h1>

                    {#if titleAditional1}
                        <h1 class="font-bold text-4xl">
                            <EditableField
                                value={titleAditional1}
                                onChange={(v) =>
                                    updateField("titleAditional1", v)}
                            />
                        </h1>
                    {/if}
                </div>

                {#if titleAditional2}
                    <h1 class="font-bold text-center text-red-600">
                        <EditableField
                            value={titleAditional2}
                            onChange={(v) => updateField("titleAditional2", v)}
                        />
                    </h1>
                {/if}
            </div>

            <div class="w-full mb-3">
                <p class="">
                    <strong style="font-size: 23px">
                        <EditableField
                            value={name}
                            onChange={(v) => updateField("name", v)}
                        />
                    </strong>
                    <EditableField
                        value={kosekiName}
                        onChange={(v) => updateField("kosekiName", v)}
                    />
                    、性別：
                    <EditableField
                        value={gender}
                        onChange={(v) => updateField("gender", v)}
                    />
                    　は、
                    <EditableField
                        value={birthDate}
                        onChange={(v) => updateField("birthDate", v)}
                    />
                    ・
                    <EditableField
                        value={birthTime}
                        onChange={(v) => updateField("birthTime", v)}
                    />
                    、
                    <EditableField
                        value={birthPlace}
                        onChange={(v) => updateField("birthPlace", v)}
                    />
                    にて出生し、 届出によりとう自然人登記役場　出生登録台帳　
                    <EditableField
                        value={registrationNun}
                        onChange={(v) => updateField("registrationNum", v)}
                    />
                    の下に登録された事を証明します。
                    {#if newBornNumber}
                        新生児口述登録
                        <EditableField
                            value={newBornNumber}
                            onChange={(v) => updateField("newBornNumber", v)}
                        />
                        。
                    {/if}
                </p>

                <div class="mt-4 w-full mb-5">
                    <div class="flex pt-4 w-full">
                        <p class="font-semibold pt-1 w-[10%]">父親氏名：</p>
                        <div class="flex pt-1 w-[90%]">
                            <EditableField
                                value={fatherName}
                                onChange={(v) => updateField("fatherName", v)}
                            />
                            {#if fatherKosekiName}
                                <EditableField
                                    value={fatherKosekiName}
                                    onChange={(v) =>
                                        updateField("fatherKosekiName", v)}
                                />
                            {/if}
                            <EditableField
                                value={fatherBirthPlace}
                                onChange={(v) =>
                                    updateField("fatherBirthPlace", v)}
                            />
                        </div>
                    </div>

                    <div class="flex w-full pb-4">
                        <p class="font-semibold pt-1 w-[10%]">母親氏名:</p>
                        <div class="flex pt-1 w-[90%]">
                            <EditableField
                                value={motherName}
                                onChange={(v) => updateField("motherName", v)}
                            />
                            {#if motherKosekiName}
                                <EditableField
                                    value={motherKosekiName}
                                    onChange={(v) =>
                                        updateField("motherKosekiName", v)}
                                />
                            {/if}
                            <EditableField
                                value={motherBirthPlace}
                                onChange={(v) =>
                                    updateField("motherBirthPlace", v)}
                            />
                        </div>
                    </div>

                    <div class="flex pt-4 w-full">
                        <p class="font-semibold pt-1 w-[15%]">父方祖父氏名：</p>
                        <div class="flex pt-1 w-[85%]">
                            <EditableField
                                value={fatherSideGrandFather}
                                onChange={(v) =>
                                    updateField("fatherSideGrandFather", v)}
                            />
                            {#if fatherSideGrandFatherKosekiName}
                                <EditableField
                                    value={fatherSideGrandFatherKosekiName}
                                    onChange={(v) =>
                                        updateField(
                                            "fatherSideGrandFatherKosekiName",
                                            v,
                                        )}
                                />
                            {/if}
                        </div>
                    </div>

                    <div class="flex pt-1 w-full pb-4">
                        <p class="font-semibold pt-1 w-[15%]">父方祖母氏名：</p>
                        <div class="flex pt-1 w-[85%]">
                            <EditableField
                                value={fatherSideGrandMother}
                                onChange={(v) =>
                                    updateField("fatherSideGrandMother", v)}
                            />
                            {#if fatherSideGrandMotherKosekiName}
                                <EditableField
                                    value={fatherSideGrandMotherKosekiName}
                                    onChange={(v) =>
                                        updateField(
                                            "fatherSideGrandMotherKosekiName",
                                            v,
                                        )}
                                />
                            {/if}
                        </div>
                    </div>

                    <div class="flex pt-4 w-full">
                        <p class="font-semibold pt-1 w-[15%]">母方祖父氏名：</p>
                        <div class="flex pt-1 w-[85%]">
                            <EditableField
                                value={motherSideGrandFather}
                                onChange={(v) =>
                                    updateField("motherSideGrandFather", v)}
                            />
                            {#if motherSideGrandFatherKosekiName}
                                <EditableField
                                    value={motherSideGrandFatherKosekiName}
                                    onChange={(v) =>
                                        updateField(
                                            "motherSideGrandFatherKosekiName",
                                            v,
                                        )}
                                />
                            {/if}
                        </div>
                    </div>

                    <div class="flex pt-1 w-full pb-4">
                        <p class="font-semibold pt-1 w-[15%]">母方祖母氏名：</p>
                        <div class="flex pt-1 w-[85%]">
                            <EditableField
                                value={motherSideGrandMother}
                                onChange={(v) =>
                                    updateField("motherSideGrandMother", v)}
                            />
                            {#if motherSideGrandMotherKosekiname}
                                <EditableField
                                    value={motherSideGrandMotherKosekiname}
                                    onChange={(v) =>
                                        updateField(
                                            "motherSideGrandMotherKosekiname",
                                            v,
                                        )}
                                />
                            {/if}
                        </div>
                    </div>
                </div>

                <div class="pb-4 pt-1">
                    <EditableField
                        value={registrationDay}
                        onChange={(v) => updateField("registrationDate", v)}
                    />
                    <EditableField
                        value={registrationPerson}
                        onChange={(v) => updateField("registrationPerson", v)}
                    />
                    <EditableField
                        value={otherRegistration}
                        onChange={(v) => updateField("otherRegistration", v)}
                    />
                </div>

                <div class="mt-4 w-full mb-3">
                    <OneLineCell
                        divStyle={" pl-3 pt-1 inline-block relative w-[99.5%]"}
                        spanTitle={"備考:"}
                        pContent={registrationAditionalInfo}
                        editable={true}
                        onUpdate={(v) =>
                            updateField("registrationAditionalInfo", v)}
                    />
                </div>
            </div>

            <div class="flex w-full mt-5 mb-3">
                <div class="flex flex-col justify-center items-center w-full">
                    <div class="">以上事実である事を証明致します。</div>

                    <div class="my-3">
                        <EditableField
                            value={notaryCity}
                            onChange={(v) => updateField("notaryCity", v)}
                        />
                        、
                        <EditableField
                            value={emissionDate}
                            onChange={(v) => updateField("emissionDate", v)}
                        />
                    </div>

                    <div
                        class="border-b-[1px] w-[40%] border-black text-center"
                    >
                        <EditableField
                            value={scrivenerSignName}
                            onChange={(v) =>
                                updateField("scrivenerSignName", v)}
                        />
                    </div>
                    <div class="">
                        <EditableField
                            value={scrivenerType}
                            onChange={(v) => updateField("scrivenerType", v)}
                        />
                    </div>
                </div>
            </div>
        </div>

        <div class="ml-4 scale-[0.9]">
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

                <div class="flex w-full my-5">
                    <div
                        class="flex flex-col justify-center items-center w-full"
                    >
                        <div class="">以上事実である事を証明致します。</div>

                        <div class="my-3">
                            <EditableField
                                value={notaryCity}
                                onChange={(v) => updateField("notaryCity", v)}
                            />
                            、
                            <EditableField
                                value={emissionDate}
                                onChange={(v) => updateField("emissionDate", v)}
                            />
                        </div>

                        <div
                            class="border-b-[1px] w-[40%] border-black text-center"
                        >
                            <EditableField
                                value={scrivenerSignName}
                                onChange={(v) =>
                                    updateField("scrivenerSignName", v)}
                            />
                        </div>
                        <div class="">
                            <EditableField
                                value={scrivenerType}
                                onChange={(v) =>
                                    updateField("scrivenerType", v)}
                            />
                        </div>
                    </div>
                </div>

                <div class="scale-[0.9]">
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
