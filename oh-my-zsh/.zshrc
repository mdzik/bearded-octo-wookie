# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/home/mdzik/.oh-my-zsh"

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
#ZSH_THEME="robbyrussell"
POWERLEVEL9K_MODE='awesome-fontconfig'

ZSH_THEME="powerlevel9k/powerlevel9k"

# Set list of themes to load
# Setting this variable when ZSH_THEME=random
# cause zsh load theme from this variable instead of
# looking in ~/.oh-my-zsh/themes/
# An empty array have no effect
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(  git   zsh-autosuggestion  zsh-completions fzf-zsh notify )


autoload -U compinit
compinit



# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
#
#
# # Set up the prompt                                                                                                                                                                                                
                                                                                                                                                                                                                   
#autoload -Uz promptinit                                                                                                                                                                                            
#promptinit                                                                                                                                                                                                         
#prompt adam1                                                                                                                                                                                                       
                                                                                                                                                                                                                   
#setopt histignorealldups sharehistory                                                                                                                                                                              
                                                                                                                                                                                                                   
# Use emacs keybindings even if our EDITOR is set to vi                                                                                                                                                            
#bindkey -e                                                                                                                                                                                                         
                                                                                                                                                                                                                   
# Keep 1000 lines of history within the shell and save it to ~/.zsh_history:                                                                                                                                       
#HISTSIZE=1000                                                                                                                                                                                                      
#SAVEHIST=1000                                                                                                                                                                                                      
#HISTFILE=~/.zsh_history                                                                                                                                                                                            
#                                                                                                                                                                                                                   
## Use modern completion system                                                                                                                                                                                     
#autoload -Uz compinit                                                                                                                                                                                              
#compinit                                                                                                                                                                                                           
#                                                                                                                                                                                                                   
#zstyle ':completion:*' auto-description 'specify: %d'                                                                                                                                                              
#zstyle ':completion:*' completer _expand _complete _correct _approximate                                                                                                                                           
#zstyle ':completion:*' format 'Completing %d'                                                                                                                                                                      
#zstyle ':completion:*' group-name ''                                                                                                                                                                               
#zstyle ':completion:*' menu select=2                                                                                                                                                                               
#eval "$(dircolors -b)"                                                                                                                                                                                             
#zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}                                                                                                                                                      
#zstyle ':completion:*' list-colors ''                                                                                                                                                                              
#zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s                                                                                                                         
#zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'                                                                                                              
#zstyle ':completion:*' menu select=long                                                                                                                                                                            
#zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s                                                                                                                                 
#zstyle ':completion:*' use-compctl false                                                                                                                                                                           
#zstyle ':completion:*' verbose true                                                                                                                                                                                
#                                                                                                                                                                                                                   
#zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'                                                                                                                                   
#zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'                                                                                                                                    
                                                                                                                                                                                                                   
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh  


source $ZSH/oh-my-zsh.sh

source $ZSH_CUSTOM/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
