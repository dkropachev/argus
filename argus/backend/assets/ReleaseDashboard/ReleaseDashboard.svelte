<script>
    export let releaseData = {};
    import { faGithub } from "@fortawesome/free-brands-svg-icons";
    import { faBug } from "@fortawesome/free-solid-svg-icons";
    import Fa from "svelte-fa";
    import ChartStats from "../Stats/ChartStats.svelte";
    import ReleaseStats from "../Stats/ReleaseStats.svelte";
    import ReleaseActivity from "./ReleaseActivity.svelte";
    import GithubIssues from "../Github/GithubIssues.svelte";
    import ReleaseGithubIssues from "./ReleaseGithubIssues.svelte";
    import TestPopoutSelector from "./TestPopoutSelector.svelte";
    import { sendMessage } from "../Stores/AlertStore";
    let clickedTests = [];

    const handleTestClick = function (e) {
        if (e.detail.start_time == 0) {
            sendMessage("info", `The test "${e.detail.name}" hasn't been run yet!"`);
            return;
        }

        if (clickedTests.findIndex((val) => val.name == e.detail.name) == -1) {
            clickedTests.push(e.detail);
            clickedTests = clickedTests;
        }
    };

    const handleDeleteRequest = function(ev) {
        clickedTests = clickedTests.filter(val => val.name != ev.detail.name);
    };
</script>

<div class="container-fluid border rounded mt-1 bg-white shadow-sm">
    <div class="row mb-2">
        <div class="col-8">
            <h1 class="display-1">{releaseData.release.name}</h1>
            <h3 class="text-muted">
                {releaseData.release.pretty_name ?? "No name"}
            </h3>
            <div class="input-group user-select-all">
                <span class="input-group-text">Github</span>
                <input
                    class="form-control"
                    type="text"
                    disabled
                    value={releaseData.release.github_repo_url}
                />
                <a
                    href={releaseData.release.github_repo_url}
                    target="_blank"
                    class="btn btn-dark"><Fa icon={faGithub} /></a
                >
                <a
                    href="{releaseData.release
                        .github_repo_url}/issues/new/choose"
                    target="_blank"
                    class="btn btn-success"><Fa icon={faBug} /></a
                >
            </div>
            <p class="text-muted">
                {releaseData.release.description ?? "No description provided."}
            </p>
        </div>
    </div>
    <div class="row mb-2">
        <div class="col-8">
            <ReleaseStats
                releaseName={releaseData.release.name}
                DisplayItem={ChartStats}
                showTestMap={true}
                horizontal={true}
                on:testClick={handleTestClick}
            />
        </div>
        <div class="col-4">
            <TestPopoutSelector
                bind:tests={clickedTests}
                on:deleteRequest={handleDeleteRequest}
                releaseName={releaseData.release.name}
            />
        </div>
    </div>
    <div class="row mb-2">
        <ReleaseGithubIssues
            release_id={releaseData.release.id}
            release_name={releaseData.release.name}
            tests={releaseData.tests}
        />
    </div>
    <div class="row mb-2">
        <ReleaseActivity releaseName={releaseData.release.name} />
    </div>
    <div class="row mb-2">
        <div class="col">
            <div class="accordion">
                <div class="accordion-item">
                    <h2 class="accordion-header">
                        <button
                            class="accordion-button collapsed"
                            type="button"
                            data-bs-toggle="collapse"
                            data-bs-target="#collapseIssues"
                        >
                            All Issues
                        </button>
                    </h2>
                    <div
                        id="collapseIssues"
                        class="accordion-collapse collapse"
                    >
                        <div class="accordion-body">
                            <GithubIssues
                                id={releaseData.release.id}
                                filter_key="release_id"
                                submitDisabled={true}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
