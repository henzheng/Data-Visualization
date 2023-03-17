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
        const typeColors: object = await d3.json("/PokemonTypeColors.json");
        const width: number = window.innerWidth;
        const height: number = window.innerHeight;
        const margin = { top: 20, right: 20, bottom: 50, left: 50 };
    
        const svg = d3.select("body")
            .append("svg")
            .attr("width", width - margin.left - margin.right)
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

        var size = d3.scaleLinear()
            .domain([0, 400])
            .range([7, 55]);
        //something might be wrong with the size function
        
        const toolTip = d3.select("body")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "#fff")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px")
            .style("display", "flex")
            .style("width", "150px")
            .style("flex-direction", "column")
            .style("align-items", "center")
            .style("justify-content", "center")
            .style("font-weight", "bold")
            .style("font-family", `'Lato', sans-serif`);

        var simulation = d3.forceSimulation()
            .force("center", d3.forceCenter().x(width / 2).y(height / 2)) //attration to center of the svg
            .force("charge", d3.forceManyBody().strength(.1)) 
            .force("collide", d3.forceCollide().strength(.2).radius(18).iterations(1)) // force that prevents overlapping

        let node = svg.append("g")
            .selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
                .attr("class", "node")
                .attr("fill",(d: Pokemon):any => typeColors[d.types[0].type.name])
                .attr("r", (d: Pokemon) => size(d.base_experience)/1.5)
                .attr("cx", width / 2)
                .attr("cy", width / 2)
                .style("fill-opacity", 0.8)
                .attr("stroke", "black")
                .style("stroke-width", 1)
                .on("mouseover", function() {
                    this.style.strokeWidth = "2px";
                    toolTip.style("opacity", 1);
                })
                .on("mousemove", (event: d3.ClientPointEvent, d: Pokemon) => {
                    toolTip.html(`
                        <p>${d.name[0].toUpperCase() + d.name.slice(1)}</p>
                        <img src="${d.sprites.front_default}" alt="${d.name}"/>
                    `)
                    .style("position", "absolute")
                    .style("left", (event.clientX + 25) + "px")
                    .style("top", (event.clientY - 30) + "px");
                })
                .on("mouseleave", function() {
                    this.style.strokeWidth = "1px";
                    toolTip.style("opacity", 0);
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
