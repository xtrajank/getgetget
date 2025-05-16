<script>
    import { base } from '$app/paths';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { redditResults } from '$lib/stores';

    let base_url = 'http://localhost:8000';
    let userQuestion = '';
    let loading = false;
    let error = null;

    async function handleSearch() {
        if (!userQuestion.trim()) return;

        loading = true;
        error = null;

        try {
            const res = await fetch(`${base_url}/api/reddit/search?question=${encodeURIComponent(userQuestion)}`)
            if (!res.ok) throw new Error(`Error: ${res.status}`)
            const json = await res.json();
            redditResults.set(json);
            await goto('/result');
        } catch (err) {
            error = 'Failed to fetch Reddit content: ' + err.message;
        } finally {
            loading = false;
        }
    }
</script>

<style>
    h1 {
        color: blue;
    }
    #main {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }

    .input-row {
        display: flex;
        gap: 20px;
        align-items: center;
    }

    #question-input {
        width: 30rem;
    }

    #submit-button {
        color: white;
        background-color: blue;
        border: blue 2px;
        cursor: pointer;
    }

    #submit-button:hover {
        border: 5px;
        color: black;
    }

    input, button {
        font-size: 1rem;
        padding: 0.6rem;
        margin: 0.5rem 0;
    }
</style>

<div id="main">
    <h1>getgetget</h1>
    <p>a Reddit search tool.</p>
    <p></p>

    <div class="input-row">
        <input
            id="question-input"
            type="text"
            placeholder="search"
            bind:value={userQuestion}
            on:keydown={(e) => e.key === 'Enter' && handleSearch}
        />
        <button id="submit-button" on:click={handleSearch} disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
        </button>
    </div>
</div>