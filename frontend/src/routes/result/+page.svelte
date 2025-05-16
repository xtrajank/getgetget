<script>
    import { redditResults } from "$lib/stores";
</script>

<style>

    #main {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    ul {
        font-size: 14px;
    }

    li {
        list-style-type: none;
    }
</style>

<div id="main">
    <h1>RESULTS</h1>

    <div>
        <ul>
            {#each $redditResults as item}
                <li>
                    <h2>{item.title}</h2>

                    {#if item.top_thread?.body}
                        <p><strong>Thread:</strong> {item.top_thread.body}</p>
                    {/if}
                    
                    {#if item.top_comment?.body}
                        <p><strong>Comment:</strong> {item.top_comment.body}</p>
                    {/if}
                </li>
            {/each}
        </ul>
    </div>
</div>
