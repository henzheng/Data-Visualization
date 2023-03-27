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
            .attr("width", width)
            .attr("height", height)
            .style("border", "2px solid black")

        // let groups = ["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"];
        let groups = Array.from(d3.group(data, (d: Pokemon) => d.types[0].type.name), ([key, value]) => ({ key, values: value }));
        console.log(groups)
        
        let color = d3.scaleOrdinal()
            .domain(groups.map((group) => group.key))
            .range(groups.map((group, i) => d3.interpolateRainbow(i / (groups.length - 1))))



        // let groupScale = d3.scaleOrdinal()
        //     .domain(["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"])
        //     .range(groupRange)
        
        

        // let groupScale = d3.scaleOrdinal()
        //     .domain(["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon"])
        //     .range(groupRange)
        
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
                }[]
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
            .domain([0, d3.max(data, (d: Pokemon) => d.base_experience)])
            .range([7, 45]);
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

        let simulation = d3.forceSimulation()
            .force("group", d3.forceManyBody().strength(.1))
            .force("center", d3.forceCenter().x(width / 2).y(height / 2))
            // .force("charge", d3.forceManyBody().strength(-.1)) 
            // .force("radial", d3.forceRadial(width / 5.5, width / 2, height / 2))
            .force("collide", d3.forceCollide().strength(.2).radius((d: any) => size(d.base_experience)).iterations(1)) // force that prevents overlapping

        const radius = 400;
        const clipPath = svg
            .append("circle")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("r", radius)
            .attr("fill", "none")
            .attr("stroke", "black")
            .attr("transform", `translate(${width / 2}, ${height/2})`)
            .style("stroke-width", 2)

        const inner = svg
            .append("circle")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("r", 200)
            .attr("fill", "none")
            .attr("stroke", "black")
            .attr("transform", `translate(${width / 2}, ${height/2})`)
            .style("stroke-width", 2)
        let node = svg.append("g")
            .selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
                .attr("class", "node")
                .attr("fill",(d: Pokemon):any => color(d.types[0].type.name))
                .attr("r", (d: Pokemon) => size(d.base_experience)/1.5)
                .attr("cx", width / 2)
                .attr("cy", width / 2)
                .style("fill-opacity", 0.8)
                .attr("stroke", "black")
                .style("stroke-width", 1)
                .on("mouseover", function() {
                    this.style.stroke = "white";
                    this.style.cursor = "pointer";
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
                    this.style.stroke = 'black';
                    toolTip.style("opacity", 0);
                })
                .on("click", (event: any, d: any) => {
                    console.log(d);
                    let pokemonData = [].push({
                        className: d.name,
                        axes: [
                            {axis: "hp", value: d.stats[0].base_stat},
                            {axis: "attack", value: d.stats[1].base_stat},
                            {axis: "defense", value: d.stats[2].base_stat},
                            {axis: "special-attack", value: d.stats[3].base_stat},
                            {axis: "special-defense", value: d.stats[4].base_stat},
                            {axis: "speed", value: d.stats[5].base_stat},
                        ]
                    })
                    // RadarChart.draw("body", pokemonData);
                })
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended)
                );
        
        const donutRadius = 400; // radius of the donut
        const circleRadius = 30; // radius of the circles
        const donutWidth = 200; // width of the donut

        simulation.nodes(data)
            .on("tick", function() {
                node.attr("cx", (d) => {
                        // calculate the distance of the node from the center of the visualization
                        const distance = Math.sqrt((d.x - width / 2) ** 2 + (d.y - height / 2) ** 2);
                        // check if the distance is within the donut radius
                        if (distance < donutRadius) {
                            // calculate the angle of the node relative to the center of the visualization
                            const angle = Math.atan2(d.y - height / 2, d.x - width / 2);
                            // calculate the position of the node on the inner circle of the donut
                            const innerX = Math.cos(angle) * (donutRadius - donutWidth / 2 - circleRadius);
                            const innerY = Math.sin(angle) * (donutRadius - donutWidth / 2 - circleRadius);
                            return innerX + width / 2;
                        } else {
                            // calculate the position of the node on the outer circle of the donut
                            const outerX = (d.x - width / 2) * (donutRadius + donutWidth / 2 - circleRadius) / distance + width / 2;
                            const outerY = (d.y - height / 2) * (donutRadius + donutWidth / 2 - circleRadius) / distance + height / 2;
                            return outerX;
                        }
                    })
                    .attr("cy", (d) => {
                        // calculate the distance and angle of the node relative to the center of the visualization (similar to cx)
                        const distance = Math.sqrt((d.x - width / 2) ** 2 + (d.y - height / 2) ** 2);
                        const angle = Math.atan2(d.y - height / 2, d.x - width / 2);
                        // check if the distance is within the donut radius
                        if (distance < donutRadius) {
                            // calculate the position of the node on the inner circle of the donut (similar to cx)
                            const innerX = Math.cos(angle) * (donutRadius - donutWidth / 2 - circleRadius);
                            const innerY = Math.sin(angle) * (donutRadius - donutWidth / 2 - circleRadius);
                            return innerY + height / 2;
                        } else {
                            // calculate the position of the node on the outer circle of the donut (similar to cx)
                            const outerX = (d.x - width / 2) * (donutRadius + donutWidth / 2 - circleRadius) / distance + width / 2;
                            const outerY = (d.y - height / 2) * (donutRadius + donutWidth / 2 - circleRadius) / distance + height / 2;
                            return outerY;
                        }
                    });
            });

        // simulation.nodes(data)
        //     // .force("collide", d3.forceCollide().strength(.5).radius(function(d){ return d.radius + nodePadding; }).iterations(1))
        //     .on("tick", function(this: d3.Simulation<d3.SimulationNodeDatum, undefined>) {
        //         node
        //         .attr("cx", (d: d3.SimulationNodeDatum) => {
        //             return (d.x = Math.max(radius, Math.min(width - radius, d.x)));
        //         })
        //         .attr("cy", (d: d3.SimulationNodeDatum) => {
        //             return (d.y = Math.max(radius, Math.min(height - radius, d.y)));
        //         });
        //     });

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
