<script lang="ts">
    import ScatterPlot from "../components/ScatterPlot.svelte";
    import CircularPacking from "../components/CircularPacking.svelte";
</script>

<section class="top-content">
    <h1 class="title">Generation I Pokemon</h1>
    <h3 class="description">A data visualization on all 151 Pokemon native to the Kanto region</h3>
</section>
<CircularPacking/>

<style scoped>
    * {
        overflow-x: hidden;
        font-family: 'Roboto Slab', serif;
    }
    .top-content {
        position: absolute;
        top: 40vh;
        left: 38vw;
        margin: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .description {
        font-size: 0.8rem;
        margin: 0;
    }
</style>