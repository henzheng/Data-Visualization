<script lang="ts">
    import { onMount } from "svelte";
    import * as d3 from "d3";

    const typeColors = {
        normal: "#c3c3e5",
        fire: "#f08030",
        water: "#6890f0",
        electric: "#f8d030",
        grass: "#78c850",
        ice: "#98d8d8",
        fighting: "#c03028",
        poison: "#a040a0",
        ground: "#e0c068",
        flying: "#a890f0",
        psychic: "#f85888",
        bug: "#a8b820",
        rock: "#b8a038",
        ghost: "#705898",
        dragon: "#7038f8",
    };

    interface Pokemon {
        id: number;
        name: string;
        types: string[];
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
        moves: string[];
        abilities: string[];
        front_sprite_url: string;
    }

    onMount(async () => {
        const data: Pokemon[] | any = await d3.json("/PokemonData.json");
        const margin = { top: 20, right: 20, bottom: 50, left: 50 };
        const width = 600 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        const canvas = d3.select("body")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr(
            "transform",
            "translate(" + margin.left + "," + margin.top + ")"
        );
        //create scales by setting the domain and range for each axis
        //the x axis here represents the pokemon id and the range is from 0 to the width
        const xScale = d3.scaleLinear().domain([0, d3.max(data, (d: Pokemon) => d.id)]).range([0, width]);
        const yScale = d3.scaleLinear().domain([0, d3.max(data, (d: Pokemon): number => d['total_base_stats'])]).range([height, 0]);

        const xAxis = canvas.append("g").attr("transform", `translate(0, ${height})`).call(d3.axisBottom(xScale));
        const yAxis = canvas.append("g").call(d3.axisLeft(yScale));

        const tooltip = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0)
        .style("font-family", `'Lato', sans-serif`);

        //creating all the circles on the scatterplot
        //.selectAll creates an empty subsection
        const circles = canvas.selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", (d: Pokemon):number => xScale(d.id))
        .attr("cy", (d: Pokemon):number => yScale(d['total_base_stats']))
        .attr("r", 3.5)
        .style("fill", (d: Pokemon):string => typeColors[d['types'][0]])
        .on("mouseover", (event, d: Pokemon) => {

            tooltip.transition().duration(200).style("opacity", 1);
            tooltip.html(
                `<b>${d.name}</b><br/><img src="${d.front_sprite_url}" alt="${d.name}"/>`
            )
            .style("background", `repeating-linear-gradient(45deg, ${typeColors[d['types'][0]]}, #fff 1px);`)
            .style("cursor", "pointer")
            .style("left", event.pageX + "px")
            .style("top", event.pageY + "px");
        })
        .on("mouseout", () => {
            tooltip.transition().duration(500).style("opacity", 0);
        })

        //creating labels for the x and y axis
        const xLabel = canvas.append("text")
        .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
        .style("text-anchor", "middle")
        .style("font-weight", "bold")
        .style("font-family", `'Lato', sans-serif`)
        .text("Pokedex Number");

        const yLabel = canvas.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - height / 2)
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .style("font-weight", "bold")
        .style("font-family", `'Lato', sans-serif`)
        .text("Base Stats");

        console.log("Scatterplot mounted")
    })
</script>