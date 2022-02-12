#!/bin/bash

set -e -u

work_dir=$(dirname $(realpath -- $0))

function parseopts() 
{
    local opt= optarg= i= shortopts=$1
    local -a longopts=() unused_argv=()

    shift
    while [[ $1 && $1 != '--' ]]; do
        longopts+=("$1")
        shift
    done
    shift

    longoptmatch() {
        local o longmatch=()
        for o in "${longopts[@]}"; do
            if [[ ${o%:} = "$1" ]]; then
                longmatch=("$o")
                break
            fi
            [[ ${o%:} = "$1"* ]] && longmatch+=("$o")
        done

        case ${#longmatch[*]} in
            1)
                opt=${longmatch%:}
                if [[ $longmatch = *: ]]; then
                    return 1
                else
                    return 0
                fi ;;
            0)
                return 255 ;;
            *)
                return 254 ;;
        esac
    }

    while (( $# )); do
        case $1 in
            --) # explicit end of options
                shift
                break
                ;;
            -[!-]*) # short option
                for (( i = 1; i < ${#1}; i++ )); do
                    opt=${1:i:1}

                    # option doesn't exist
                    if [[ $shortopts != *$opt* ]]; then
                        OPTRET=(--)
                        return 1
                    fi

                    OPTRET+=("-$opt")
                    # option requires optarg
                    if [[ $shortopts = *$opt:* ]]; then
                        if (( i < ${#1} - 1 )); then
                            OPTRET+=("${1:i+1}")
                            break
                        elif (( i == ${#1} - 1 )) && [[ "$2" ]]; then
                            OPTRET+=("$2")
                            shift
                            break
                        # parse failure
                        else
                            OPTRET=(--)
                            return 1
                        fi
                    fi
                done
                ;;
            --?*=*|--?*) # long option
                IFS='=' read -r opt optarg <<< "${1#--}"
                longoptmatch "$opt"
                case $? in
                    0)
                        if [[ $optarg ]]; then
                            OPTRET=(--)
                            return 1
                        else
                            OPTRET+=("--$opt")
                        fi
                        ;;
                    1)
                        if [[ $optarg ]]; then
                            OPTRET+=("--$opt" "$optarg")
                        elif [[ "$2" ]]; then
                            OPTRET+=("--$opt" "$2" )
                            shift
                        else
                            printf "%s: 配置选项 '--%s' 需要参数!\n" "${0##*/}" "$opt"
                            OPTRET=(--)
                            return 1
                        fi
                        ;;
                    254)
                        OPTRET=(--)
                        return 1
                        ;;
                    255)
                        # parse failure
                        printf "%s: 未定义的配置选项 '%s'\n" "${0##*/}" "--$opt"
                        OPTRET=(--)
                        return 1
                        ;;
                esac
                ;;
            *) # non-option arg encountered, add it as a parameter
                unused_argv+=("$1")
                ;;
        esac
        shift
    done

    # add end-of-opt terminator and any leftover positional parameters
    OPTRET+=('--' "${unused_argv[@]}" "$@")
    unset longoptmatch

    return 0
}

function cleanup()
{
    exit ${1:-$?}
}


# DJ-
function usage() 
{
cat <<EOF
使用: ${0##*/} [配置选项]

  配置选项:
   -u, --update                 更新所有数据 
   -h, --help                   显示此帮助信息并退出

EOF
}

function update_info()
{
    i=0
    j=0
    str=''
    progress=0
    # 输入: 股票名字、股票代码、当前时间
    . ${work_dir}/data/stock.sh
    total="${#stock[@]}"
    for k in $(echo ${!stock[*]})
    do
        code="${k}"
        name="${stock[$k]}"
        time=$(date "+%F")
        i=$(($i+1))
        progress=`echo "scale=2; $i/$total*100" | bc`
        python ${work_dir}/bin/k-day.py "${work_dir}/data/" "${name}" "${code}" "${time}" >/dev/null 2>&1
        if [ `echo "$j < $progress" | bc` -eq 1 ]
        then
            j=$(($j+1))
            #str+='#'
            str=#${str}
        fi
        printf "[%-100s] %02.2f  %s\r" "$str" "$progress" "${name}"
    done
}

### main
trap 'cleanup 130' INT
trap 'cleanup 143' TERM

if [ "$#" -lt 1 ]; then
    usage
    cleanup 1
fi

_opt_short='uh'
_opt_long=('update' 'help')

parseopts "$_opt_short" "${_opt_long[@]}" -- "$@" || exit 1
set -- "${OPTRET[@]}"
unset _opt_short _opt_long OPTRET

while :; do
    case $1 in
        -u|--update)                        # 更新数据
            #shift
            update_info
            ;;
        -h|--help)
            usage
            cleanup 0
            ;;
        --)
            shift
            break 2
            ;;
    esac
    shift
done


