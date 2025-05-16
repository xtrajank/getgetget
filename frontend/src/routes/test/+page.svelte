<h1>TEST</h1>
<p></p>
<script>
    let base_url = 'http://localhost:8000';
    let service = "";
    let endpoint = "";
    let data = null;
    let error = null;

    async function testFetch() {
        if (!service || !endpoint) {
            error = "Both service and endpoint required";
            return;
        }

        try {
            const res = await fetch(`${base_url}/${service}/${endpoint}`)
            if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
            data = await res.json();
            error = null;
        } catch (err) {
            error = 'Failed to fetch from backend: ' + err.message;
        }
    }
</script>

<style>
    #test {
        margin: 10px;
    }

    input, button {
        margin: 0.5rem;
        padding: 0.5rem;
        font-size: 1rem;
    }

    .json-container {
        max-width: 90vw;  
        max-height: 70vh;        
        overflow: auto;          
        margin: 0 auto;           
        padding: 1rem;
        color: black;
        font-family: 'Roboto Mono', monospace;
        border-radius: 8px;
        font-size: 14px;
    }
</style>

<div id="test">
    <input 
        placeholder="Service"
        bind:value={service}
    />
    <input 
        placeholder="Endpoint"
        bind:value={endpoint}
    />
    <button on:click={testFetch}>Fetch Data</button>
</div>

{#if error}
    <p style="color: red;">{error}</p>
{/if}

{#if data}
    <div class="json-container">
        <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
{/if}