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
        stats: object[];
        moves: string[];
        abilities: string[];
        front_sprite_url: string;
    }

    onMount(async () => {
        const data: object[] | any = await d3.json("/pokemon_data.json");
        const margin = { top: 20, right: 20, bottom: 50, left: 50 };
        const width = 600 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        // create SVG element
        const svg = d3
            .select("body")
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr(
                "transform",
                "translate(" + margin.left + "," + margin.top + ")"
            );

        // create scales for x and y axes
        const xScale = d3
            .scaleLinear()
            .domain([0, d3.max(data, (d: Pokemon) => d.id)])
            .range([0, width]);

        const yScale = d3.scaleLinear().domain([0, 120]).range([height, 0]);

        // create x axis
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(xScale));

        // create y axis
        svg.append("g").call(d3.axisLeft(yScale));

        // create tooltip
        const tooltip = d3
            .select("body")
            .append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        // create circles for each data point
        const circles = svg
            .selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", (d: Pokemon) => xScale(d.id))
            .attr("cy", (d: Pokemon) =>
                yScale(
                    d.stats.find((s) => s["stat"].name === "hp")["base_stat"]
                )
            )
            .attr("r", 5)
            .style("fill", (d: Pokemon) => typeColors[d.types[0]])
            .on("mouseover", (event, d: Pokemon) => {
                console.log(event);
                tooltip.transition().duration(200).style("opacity", 0.9);
                tooltip
                    .html(
                        `<b>${d.name}</b><br/><img src="${d.front_sprite_url}" alt="${d.name}"/>`
                    )
                    .style("left", event.pageX + "px")
                    .style("top", event.pageY - 28 + "px");
            })
            .on("mouseout", () => {
                tooltip.transition().duration(500).style("opacity", 0);
            });
        // create x axis label
        svg.append("text")
            .attr(
                "transform",
                "translate(" +
                    width / 2 +
                    " ," +
                    (height + margin.top + 30) +
                    ")"
            )
            .style("text-anchor", "middle")
            .text("Pokemon ID");

        // create y axis label
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x", 0 - height / 2)
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("Base Stats");
    });
</script>

<h1>Welcome to SvelteKit</h1>
<p>
    Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation
</p>
