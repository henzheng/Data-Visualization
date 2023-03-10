<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<svg id="canvas" width="600" height="400"></svg>

<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    onMount(() => {
        const data = [10, 100, 50, 35]
        const canvas = d3.select('#canvas');
        const circles = canvas.selectAll('circle')
        .data(data);
        circles.enter().append('circle')
        .attr('cx', 100)
        .attr('cy', 50)
        .attr('r', 50)
        .attr('fill', 'red')
    })
</script>