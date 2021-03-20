size = 13
left = size * 2 - 5
top = 5


frame = [
# FIRST LEVEL
                           [[left+ size*0,top],[left+ size*5,top],

                            [left+ size*0,top+1],[left+ size*1,top+1],
                            [left+ size*4,top+1],[left+ size*5,top+1],

                            [left+ size*0,top+2],[left+ size*1,top+2],
                            [left+ size*2,top+2],[left+ size*3,top+2],
                            [left+ size*4,top+2],[left+ size*5,top+2],

                            [left+ size*1,top+3],[left+ size*2,top+3],
                            [left+ size*3,top+3],[left+ size*4,top+3],

                            [left+ size*2,top+4],[left+ size*3,top+4],

                            [left+ size*2,top+6],[left+ size*3,top+6],

                            [left+ size*1,top+7],[left+ size*2,top+7],
                            [left+ size*3,top+7],[left+ size*4,top+7],

                            [left+ size*0,top+8],[left+ size*1,top+8],
                            [left+ size*2,top+8],[left+ size*3,top+8],
                            [left+ size*4,top+8],[left+ size*5,top+8],

                            [left+ size*2,top+9],[left+ size*3,top+9]],

# SECOND LEVEL
                            [[left+ size*0,top],[left+ size*5,top],


                            [left+ size*0,top+2],[left+ size*1,top+2],
                            [left+ size*2,top+2],[left+ size*3,top+2],
                            [left+ size*4,top+2],[left+ size*5,top+2],


                            [left+ size*1,top+4],[left+ size*4,top+4],

                            [left+ size*1,top+5],[left+ size*4,top+5],
                            [left+ size*1,top+5],[left+ size*4,top+6],
                            [left+ size*1,top+7],[left+ size*4,top+7],



                            [left+ size*0,top+8],[left+ size*1,top+8],
                            [left+ size*2,top+8],[left+ size*3,top+8],
                            [left+ size*4,top+8],[left+ size*5,top+8],

                            [left+ size*2,top+9],[left+ size*3,top+9]],

# BOSS LEVEL
                            [


                            [left+ size*1,top+3],[left+ size*2,top+3],
                            [left+ size*3,top+3],[left+ size*4,top+3],

                            [left+ size*2,top+4],[left+ size*3,top+4],

                            [left+ size*2,top+6],[left+ size*3,top+6],

                            [left+ size*1,top+7],[left+ size*2,top+7],
                            [left+ size*3,top+7],[left+ size*4,top+7],

                            [left+ size*1,top+8],
                            [left+ size*2,top+8],[left+ size*3,top+8],
                            [left+ size*4,top+8],

                            [left+ size*2,top+9],[left+ size*3,top+9]],

                    ]

power_frame = [
# FIRST LEVEL
                               [5, 0,

                                1, 2,
                                2, 1,

                                5, 0,
                                0, 0,
                                6, 6,

                                3, 3,
                                4, 4,

                                0, 0,
                                0, 0,

                                4, 3,
                                1, 2,

                                2, 3,
                                8, 8,
                                8, 8,

                                8, 8],
# SECOND LEVEL
                               [5, 0,

                                5, 0,
                                1, 2,
                                6, 6,

                                4, 4,

                                6, 6,
                                0, 0,
                                6, 6,

                                7, 7,
                                5, 5,
                                7, 7,

                                0,0],
# BOSS LEVEL
                               [

                                0, 0,
                                0, 0,

                                0, 0,
                                0, 0,

                                0, 0,
                                0, 0,

                                0,
                                0, 0,
                                0,

                                0, 0],
                        ]

brick_strength_frame = [
# FIRST LEVEL
                                        [4, 4,

                                        4, 4,
                                        4, 4,

                                        4, 4,
                                        2, 3,
                                        3, 1,

                                        1, 1,
                                        1, 1,

                                        3, 1,
                                        2, 1,

                                        2, 2,
                                        0, 0,

                                        -1, -2,
                                        -3, -3,
                                        -1, -3,

                                        0, 0],


#SECOND LEVEL

                                       [1, 3,

                                        4, 4,
                                        2, 3,
                                        4, 4,

                                        3, 1,

                                        4, 4,
                                        4, 4,
                                        4, 4,


                                        -1, -2,
                                        -3, -3,
                                        -1, -3,

                                        0, 0],

# BOSS LEVEL

                                       [
                                        0, 0,
                                        0, 0,

                                        0, 0,
                                        0, 0,

                                        0, 0,
                                        0, 0,

                                        0,
                                        0, 0,
                                        0,

                                        0, 0],
]


weak_one = [
                        [left+ size*0,top],[left+ size*1,top],
                        [left+ size*2,top],[left+ size*3,top],
                        [left+ size*4,top],[left+ size*5,top],
           ]

weak_two = [
                        [left+ size*0,top+1],[left+ size*1,top+1],
                        [left+ size*2,top+1],[left+ size*3,top+1],
                        [left+ size*4,top+1],[left+ size*5,top+1],
           ]