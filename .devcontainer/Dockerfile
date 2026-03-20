# ============================================================================
# Devcontainer: Claude Code + ai-jail (non-root)
# ============================================================================
# Base: Node 20 on Debian Bookworm (slim) — avoids musl issues with Claude CLI
FROM mcr.microsoft.com/devcontainers/typescript-node:1-20-bookworm

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# ── System dependencies ─────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    # ai-jail requirement (Linux sandbox backend)
    bubblewrap \
    # General dev tools
    git \
    curl \
    wget \
    ca-certificates \
    gnupg \
    sudo \
    # Research / paper tooling
    pandoc \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-xetex \
    lmodern \
    latexmk \
    # Python for research scripts
    python3 \
    python3-pip \
    python3-venv \
    # Useful for AI agents
    ripgrep \
    fd-find \
    jq \
    tree \
    texlive-plain-generic \
    && rm -rf /var/lib/apt/lists/* \
    && fmtutil-sys --all

# ── Create non-root user ────────────────────────────────────────────────────
# node:20 ships with user "node" at UID/GID 1000 — remove it first so we
# can reclaim that UID/GID for vscode.
RUN userdel -r node 2>/dev/null || true \
    && groupdel node 2>/dev/null || true \
    && groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} -s /bin/bash \
    && echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}


# ── Install Claude Code CLI via native installer (as non-root user) ─────────
USER ${USERNAME}
RUN curl -fsSL https://claude.ai/install.sh | bash
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
# Switch back to root for remaining system-level installs
USER root

# ── Install ai-jail from GitHub Releases ────────────────────────────────────
ARG AI_JAIL_VERSION=latest
RUN ARCH=$(dpkg --print-architecture) \
    && case "${ARCH}" in \
    amd64) AI_JAIL_ARCH="x86_64" ;; \
    arm64) AI_JAIL_ARCH="aarch64" ;; \
    *) echo "Unsupported architecture: ${ARCH}" && exit 1 ;; \
    esac \
    && if [ "${AI_JAIL_VERSION}" = "latest" ]; then \
    DOWNLOAD_URL="https://github.com/akitaonrails/ai-jail/releases/latest/download/ai-jail-linux-${AI_JAIL_ARCH}.tar.gz"; \
    else \
    DOWNLOAD_URL="https://github.com/akitaonrails/ai-jail/releases/download/${AI_JAIL_VERSION}/ai-jail-linux-${AI_JAIL_ARCH}.tar.gz"; \
    fi \
    && curl -fsSL "${DOWNLOAD_URL}" | tar xz -C /usr/local/bin/ \
    && chmod +x /usr/local/bin/ai-jail

# ── Prepare directories owned by non-root user ─────────────────────────────
RUN mkdir -p /home/${USERNAME}/.claude \
    && mkdir -p /home/${USERNAME}/.config \
    && mkdir -p /home/${USERNAME}/.cache \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}

# ── Switch to non-root user ─────────────────────────────────────────────────
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Verify installations run as non-root
RUN node --version && claude --version && ai-jail --version