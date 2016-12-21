-- annotation test

{
    ['a'] = "first item", -- this is an annotation
    ['b'] = "-- this is not an annotaion",
    -- this is an annotation
    ['c'] =
    {
        --[[
            this is multi annotations
            " this is not a string "
            this is multi annotations
        ]]
        'd',
        
        --[==[
            this is multi annotations
            " this is not a string "
            this is multi annotations
        ]==]
        'e',
        --[====[
            this is multi annotations
            " this is not a string "
            this is multi annotations
        ]====]
    }
}