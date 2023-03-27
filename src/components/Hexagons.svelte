<script lang="ts">
    import { onMount } from 'svelte';
    import * as d3 from "d3";
    import { select, selectAll } from 'd3';
    import { hexbin } from "d3-hexbin";
    const width = 600;
    const height = 600;
    const margin = { top: 20, right: 20, bottom: 20, left: 20 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;
    
    let svg;
    let hexagons;
    
    onMount(async () => {
        
        svg = select('#hexagonal-heatmap')
        .append('svg')
        .attr('width', width)
        .attr('height', height);
        
        hexagons = svg
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
        
      // create the hexagonal heatmap
      createHexagonalHeatmap();
    });
    
    async function createHexagonalHeatmap() {
      const pokemonData: object[] = await d3.json("/PokemonData.json");
      // create the hexagonal layout
      const hexbinLayout = hexbin().size([innerWidth, innerHeight]).radius(20);
  
      // create the hexagonal bins
      const bins = hexbinLayout(pokemonData.map((d: any) => [d.x, d.y]));
      const colors = await d3.json("/PokemonTypeColors.json");
      // create the hexagonal paths
      hexagons
        .selectAll('.hexagon')
        .data(bins)
        .join('path')
        .attr('class', 'hexagon')
        .attr('d', d => `M${d.x},${d.y}${hexbin.hexagon()}`)
        .style('fill', d => colors[d[0].type1])
        .style('stroke', 'white')
        .style('stroke-width', 1);
    }
  </script>
  
  <div id="hexagonal-heatmap"></div>
  
  <style>
    .hexagon {
      cursor: pointer;
    }
  </style>
  