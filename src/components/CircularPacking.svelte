<script lang="ts">
    import * as d3 from "d3";
    import { onMount } from "svelte";
    onMount(async () => {
        const res = await fetch("https://pokeapi.co/api/v2/pokemon?limit=151");
        const pokemonJSON = await res.json();
        const allPokemon = pokemonJSON.results;
        let data = [];
        
        await allPokemon.forEach(async (e) => {
            const res = await fetch(e.url);
            data.push(await res.json());
        });
        console.log(data)
        
        const width: number = window.innerWidth;
        const height: number = window.innerHeight;
        // const sizeDivisor: number = 100;
        // const nodePadding: number = 2.5;
    
        const svg = d3.select("body")
            .append("svg")
            .attr("width", width)
            .attr("height", height)

        var color = d3.scaleOrdinal()
            .domain(["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"])
            .range(["#A8A878","#F08030","#6890F0","#F8D030","#78C850","#98D8D8","#C03028","#A040A0","#E0C068","#A890F0","#F85888","#A8B820","#B8A038","#705898","#7038F8"]);
        
        interface Pokemon {
            id: number;
            name: string;
            base_experience: number;
            sprites: {
                front_default: string;
            };
            stats: [
                {
                    base_stat: number;
                    effort: number;
                    stat: {
                        name: string;
                        url: string;
                    }
                }
            ];
            types: [
                {
                    slot: number;
                    type: {
                        name: string;
                        url: string;
                    }
                }
            ];
            moves: object[];
            abilities: object[];
            [key: string]: any;
        }

        function getTotalBaseStats(pokemon: Pokemon):number {
            let totalStats = 0;
            for(let i=0; i<pokemon.stats.length; i++) {
                totalStats += pokemon.stats[i].base_stat;
            }
            return totalStats;
        }

        var size = d3.scaleLinear()
            .domain([0, 40000000])
            .range([7, 550000]);
        //something is wrong with the size function
        
        const toolTip = d3.select("body")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "#fff")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px");

        var simulation = d3.forceSimulation()
            .force("center", d3.forceCenter().x(width / 2).y(height / 2)) //attration to center of the svg
            .force("charge", d3.forceManyBody().strength(.1)) 
            .force("collide", d3.forceCollide().strength(.2).radius((d: any) => size(d.value)+3).iterations(1)) // force that prevents overlapping
        
        var graph: Object[] | any = await d3.json("PokemonData.json");
        graph = graph.sort((a, b) => b.size - a.size);

        let node = svg.append("g")
            .selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
                .attr("class", "node")
                .attr("fill",(d: Pokemon):any => color(d.types[0].type.name))
                .attr("r", (d: Pokemon) => d.base_experience / 5)
                .attr("cx", width / 2)
                .attr("cy", width / 2)
                .style("fill-opacity", 0.8)
                .attr("stroke", "black")
                .style("stroke-width", 1)
                .on("mouseover", () => {
                    toolTip.style("opacity", 1);
                })
                .on("mousemove", (event, d: Pokemon) => {
                    toolTip.html(`
                        <u>${d.name}</u>
                        <br>
                        <span>Base Experience: ${d.base_experience}</span>
                    `)
                    .style("left", (event.x/2+20) + "px")
                    .style("top", (event.x/2-30) + "px");
                })
                .on("mouseleave", () => {
                    toolTip.style("opacity", 0)
                })
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended)
                );

        simulation.nodes(data)
            // .force("collide", d3.forceCollide().strength(.5).radius(function(d){ return d.radius + nodePadding; }).iterations(1))
            .on("tick", function(this: d3.Simulation<d3.SimulationNodeDatum, undefined>) {
                node
                .attr("cx", (d: d3.SimulationNodeDatum) => d.x)
                .attr("cy", (d: d3.SimulationNodeDatum) => d.y);
            });

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(.03).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(.03);
            d.fx = null;
            d.fy = null;
        }
        console.log("Created Simulation!")
    })

</script>
