<script>

    function printDiv () {

        const printContents = document.getElementById('printableDiv').innerHTML
        const originalContents = document.body.innerHTML

        document.body.innerHTML = printContents

        window.print()

        document.body.innerHTML = originalContents
        window.location.reload()
    }


</script>

<div class="flex justify-center my-4">

    <button class="
        my-4 
        h-14 w-44 
        bg-black 
        text-2xl text-white font-bold 
        rounded-lg hover:scale-[1.1]
        " 
        on:click={printDiv}>印刷</button>
</div>


<div id='printableDiv' class="flex flex-col items-center">

    <!--Front Page Container Start-->
    <div class='
        w-[213mm] h-[305mm]
        flex flex-col
        '>





    </div>
    <!--Front Page Container End-->



    <!--Back Page Container Start-->
    <div class='
        w-[213mm] h-[305mm]
        flex flex-col
        '>


        

    </div>
    <!--Back Page Container End-->

</div>

<style>
    @media print {
        #printableDiv {
            display: block;
            align-items: normal;
            justify-content: normal;
        }
    }
</style>