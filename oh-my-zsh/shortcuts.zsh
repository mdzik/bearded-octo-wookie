# You can put files here to add functionality separated per file, which
# will be ignored by git.
# Files on the custom/ directory will be automatically loaded by the init
# script, in alphabetical order.

# For example: add yourself some shortcuts to projects you often work on.
#
# brainstormr=~/Projects/development/planetargon/brainstormr
# cd $brainstormr

d_cases='\/home\/mdzik\/cases\/'
neptun_cases='/mnt/neptun/mdzik/cases'
prometheus_cases='/net/scratch/people/plgmdzikowski/cases'

function neptun() {
    ssh neptun
}

function prometheus() {
    if test ! -e "~/.ssh/prometheus:22";
    then
      pass -c plgrid/main 
    fi
    ssh prometheus
}



function from_host {
    v="sed s/$d_cases//g"
    d=$( pwd | ${(z)v} )

    if [[ "x$3" = "x" ]]
    then
        m="*[npz,csv,xml]"
    else
        m=$3
    fi
    
    r=" $1:'$2/$d/' ./"
    echo "Running: $r"
    sleep 3 
    rsync  --include='*/' --include="$m" --exclude='*' -h -a -P --info=progress  ${(z)r}

    notify-send "Transfer finished"
}
function to_host {
#    set -e
#    set -x

    if [[ "x$3" = "x" ]]
    then
        m="*[xml,py]"
    else
        m=$3
    fi
    v="sed s/$d_cases//g"
    d=$( pwd | ${(z)v} )
    r="./ $1:'$2/$d/'"
    echo "Running: ${(z)r}"
    sleep 3 
    
    rsync  --include='*/' --include="$m" --exclude='*' -h -a -P --info=progress  ${(z)r}
    
    notify-send "Transfer finished"

#    set +e
 #   set +x
}

function from_neptun {
    from_host "neptun" "$neptun_cases"
}
function to_neptun {
    to_host "neptun" "$neptun_cases"
}

function from_pr {
    from_host "prometheus" "$prometheus_cases" $1
}
function to_pr {
    to_host "prometheus" "$prometheus_cases" $1
}


function make_tclb {
    d=`pwd`
    cd /home/mdzik/projekty/TCLB 
    make $1 $2
    notify-send "TCLB build finished"
    cd $d
}



function tclb {
    mpirun -np 1 ~/projekty/TCLB/CLB/$1/main $2 $3 $4
}


function _findtclb {

	local curcontext="$curcontext" state line
	typeset -A opt_args

	_arguments -C \
		':command:->command' \
        '*: :_files'
#		'*::options:->options'

	case $state in
		(command)

			local -a subcommands
			subcommands=(
			    $(ls ~/projekty/TCLB/CLB/| grep -e '^d*' )
			)
			_describe -t commands 'tclb' subcommands
		;;
    esac
}


compdef _findtclb tclb 
