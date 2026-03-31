# credits: https://github.com/deependujha

from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

Optional_Str = Annotated[Optional[str], Field(description="An optional string value.")]


class RepoPR(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    repo_org: Optional_Str = Field(None, description="The organization or user that owns the repository.")
    repo_name: Optional_Str = Field(None, description="The name of the repository.")
    repository: Optional_Str = Field(None, description="The full name of the repository in the format 'owner/repo'.")
    pr_number: int = Field(..., description="The number of the pull request.")

    @model_validator(mode="after")
    def check_repo_info(self):
        if self.repository is None and (self.repo_org is None or self.repo_name is None):
            raise ValueError(
                "Either 'repository' or both 'repo_org' and 'repo_name' must be provided."
                f"Got: {self.repository=}, {self.repo_org=}, {self.repo_name=}"
            )
        if self.repository is not None and (self.repo_org is not None or self.repo_name is not None):
            raise ValueError(
                "Provide either 'repository' or both 'repo_org' and 'repo_name', not both."
                f"Got: {self.repository=}, {self.repo_org=}, {self.repo_name=}"
            )
        return self


class PRStatus(BaseModel):
    error_occured: bool = Field(False, description="Indicates if an error occurred while fetching PR status.")
    error_msg: Optional_Str = Field(None, description="The error message if an error occurred.")
    pr_number: int = Field(..., description="The number of the pull request.")
    title: str = Field(..., description="The title of the pull request.")
    last_commit_sha: str = Field(..., description="The SHA of the last commit in the pull request.")
    ci_check_passed: bool = Field(..., description="Whether the CI checks have passed for the pull request.")
    is_merged: bool = Field(..., description="Whether the pull request has been merged.")
    is_closed: bool = Field(..., description="Whether the pull request has been closed.")
