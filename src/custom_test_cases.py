"""
Custom test cases for text-to-SQL evaluation.

These test cases cover diverse SQL patterns to ensure comprehensive evaluation:
- HAVING clause queries
- Multiple joins with aggregation
- Date grouping and filtering
- String pattern matching
- Aggregation with calculations
"""

CUSTOM_TEST_CASES = [
    {
        "question": "Which artists have more than 10 albums?",
        "sql": "SELECT ar.Name, COUNT(al.AlbumId) as AlbumCount FROM Artist ar JOIN Album al ON ar.ArtistId = al.ArtistId GROUP BY ar.ArtistId, ar.Name HAVING COUNT(al.AlbumId) > 10 ORDER BY AlbumCount DESC",
        "expected_result": [
            {
                "Name": "Iron Maiden",
                "AlbumCount": 21
            },
            {
                "Name": "Led Zeppelin",
                "AlbumCount": 14
            },
            {
                "Name": "Deep Purple",
                "AlbumCount": 11
            }
        ],
        "category": "aggregation_with_having",
    },
    {
        "question": "What are the top 3 customers by total spending?",
        "sql": "SELECT c.FirstName || ' ' || c.LastName as CustomerName, SUM(i.Total) as TotalSpending FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId, c.FirstName, c.LastName ORDER BY TotalSpending DESC LIMIT 3",
        "expected_result": [
            {
                "CustomerName": "Helena Holý",
                "TotalSpending": 49.62
            },
            {
                "CustomerName": "Richard Cunningham",
                "TotalSpending": 47.62
            },
            {
                "CustomerName": "Luis Rojas",
                "TotalSpending": 46.62
            }
        ],
        "category": "aggregation_with_joins",
    },
    {
        "question": "How many tracks were sold in each month of 2013?",
        "sql": "SELECT strftime('%Y-%m', InvoiceDate) as Month, SUM(Quantity) as TracksSold FROM Invoice i JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId WHERE strftime('%Y', InvoiceDate) = '2013' GROUP BY Month ORDER BY Month",
        "expected_result": [],
        "category": "date_grouping",
    },
    {
        "question": "Which tracks contain the word 'love' in their name?",
        "sql": "SELECT Name, Composer FROM Track WHERE Name LIKE '%love%' OR Name LIKE '%Love%' ORDER BY Name",
        "expected_result": [
            {
                "Name": "(I Can't Help) Falling In Love With You",
                "Composer": None
            },
            {
                "Name": "(There Is) No Greater Love (Teo Licks)",
                "Composer": "Isham Jones & Marty Symes"
            },
            {
                "Name": "Ain't Talkin' 'Bout Love",
                "Composer": "Edward Van Halen, Alex Van Halen, Michael Anthony and David Lee Roth"
            },
            {
                "Name": "Ain't Talkin' 'bout Love",
                "Composer": "Edward Van Halen, Alex Van Halen, David Lee Roth, Michael Anthony"
            },
            {
                "Name": "All My Love",
                "Composer": "Robert Plant & John Paul Jones"
            },
            {
                "Name": "All My Love",
                "Composer": "E. Schrody/L. Dimant"
            },
            {
                "Name": "Arms Around Your Love",
                "Composer": "Chris Cornell"
            },
            {
                "Name": "Believe in Love",
                "Composer": None
            },
            {
                "Name": "Calling Dr. Love",
                "Composer": "Gene Simmons"
            },
            {
                "Name": "Cascades : I'm Not Your Lover",
                "Composer": "Ian Gillan, Roger Glover, Jon Lord, Steve Morse, Ian Paice"
            },
            {
                "Name": "Crazy Little Thing Called Love",
                "Composer": "Mercury, Freddie"
            },
            {
                "Name": "Cry For Love",
                "Composer": "Bossi/David Coverdale/Earl Slick"
            },
            {
                "Name": "Dirty Love",
                "Composer": "Clarke/Kilmister/Taylor"
            },
            {
                "Name": "Do You Feel Loved",
                "Composer": "Bono, The Edge, Adam Clayton, and Larry Mullen"
            },
            {
                "Name": "Do You Have Other Loves?",
                "Composer": None
            },
            {
                "Name": "Do You Love Me",
                "Composer": "Paul Stanley, B. Ezrin, K. Fowley"
            },
            {
                "Name": "Do You Love Me",
                "Composer": "Paul Stanley, Bob Ezrin, Kim Fowley"
            },
            {
                "Name": "Don't Take Your Love From Me",
                "Composer": None
            },
            {
                "Name": "Everlasting Love",
                "Composer": "Buzz Cason/Mac Gayden"
            },
            {
                "Name": "Feel Your Love Tonight",
                "Composer": "Edward Van Halen, Alex Van Halen, Michael Anthony and David Lee Roth"
            },
            {
                "Name": "Freestyle Love",
                "Composer": None
            },
            {
                "Name": "Get Down, Make Love",
                "Composer": "Mercury"
            },
            {
                "Name": "Give Me Love",
                "Composer": "Caetano Veloso e Gilberto Gil"
            },
            {
                "Name": "Gonna Give Her All The Love I've Got",
                "Composer": "Barrett Strong/Norman Whitfield"
            },
            {
                "Name": "Gonna Keep On Tryin' Till I Win Your Love",
                "Composer": "Barrett Strong/Norman Whitfield"
            },
            {
                "Name": "Good Old-Fashioned Lover Boy",
                "Composer": "Mercury, Freddie"
            },
            {
                "Name": "Heavy Love Affair",
                "Composer": "Marvin Gaye"
            },
            {
                "Name": "House Of Love",
                "Composer": "Jimmy Page, Robert Plant, Charlie Jones, Michael Lee"
            },
            {
                "Name": "I Heard Love Is Blind",
                "Composer": None
            },
            {
                "Name": "I Need Love",
                "Composer": "Bolin/Coverdale"
            },
            {
                "Name": "I Still Love You",
                "Composer": "Paul Stanley"
            },
            {
                "Name": "Is This Love",
                "Composer": "Sykes"
            },
            {
                "Name": "Is This Love (Live)",
                "Composer": None
            },
            {
                "Name": "It's Only Love",
                "Composer": "Jimmy and Vella Cameron"
            },
            {
                "Name": "Jesus Of Suburbia / City Of The Damned / I Don't Care / Dearly Beloved / Tales Of Another Broken Home",
                "Composer": "Billie Joe Armstrong/Green Day"
            },
            {
                "Name": "Let Love Rule",
                "Composer": "Lenny Kravitz"
            },
            {
                "Name": "Let Me Love You Baby",
                "Composer": "Willie Dixon"
            },
            {
                "Name": "Let Me Love You Baby",
                "Composer": "Willie Dixon"
            },
            {
                "Name": "Living On Love",
                "Composer": "Bossi/David Coverdale/Earl Slick"
            },
            {
                "Name": "Looking For Love",
                "Composer": "Sykes"
            },
            {
                "Name": "Loud Love",
                "Composer": "Chris Cornell"
            },
            {
                "Name": "Love",
                "Composer": None
            },
            {
                "Name": "Love Ain't No Stranger",
                "Composer": "Galley"
            },
            {
                "Name": "Love And Marriage",
                "Composer": "jimmy van heusen/sammy cahn"
            },
            {
                "Name": "Love And Peace Or Else",
                "Composer": "Adam Clayton, Bono, Larry Mullen & The Edge"
            },
            {
                "Name": "Love Bites",
                "Composer": None
            },
            {
                "Name": "Love Boat Captain",
                "Composer": "Eddie Vedder"
            },
            {
                "Name": "Love Child",
                "Composer": "Bolin/Coverdale"
            },
            {
                "Name": "Love Comes",
                "Composer": "Darius \"Take One\" Minwalla/Jon Auer/Ken Stringfellow/Matt Harris"
            },
            {
                "Name": "Love Comes Tumbling",
                "Composer": "U2"
            },
            {
                "Name": "Love Conquers All",
                "Composer": "Blackmore, Glover, Turner"
            },
            {
                "Name": "Love Don't Mean a Thing",
                "Composer": "D.Coverdale/G.Hughes/Glenn Hughes/I.Paice/Ian Paice/J.Lord/John Lord/R.Blackmore/Ritchie Blackmore"
            },
            {
                "Name": "Love Gun",
                "Composer": "Paul Stanley"
            },
            {
                "Name": "Love In An Elevator",
                "Composer": "Steven Tyler, Joe Perry"
            },
            {
                "Name": "Love Is Blind",
                "Composer": "David Coverdale/Earl Slick"
            },
            {
                "Name": "Love Is Blindness",
                "Composer": "U2"
            },
            {
                "Name": "Love Is Strong",
                "Composer": "Jagger/Richards"
            },
            {
                "Name": "Love Is The Colour",
                "Composer": "R. Carless"
            },
            {
                "Name": "Love Is a Losing Game",
                "Composer": None
            },
            {
                "Name": "Love Me Darlin'",
                "Composer": "C. Burnett"
            },
            {
                "Name": "Love Me Like A Reptile",
                "Composer": "Clarke/Kilmister/Taylor"
            },
            {
                "Name": "Love Of My Life",
                "Composer": "Carlos Santana & Dave Matthews"
            },
            {
                "Name": "Love Or Confusion",
                "Composer": "Jimi Hendrix"
            },
            {
                "Name": "Love Removal Machine",
                "Composer": None
            },
            {
                "Name": "Love Rescue Me",
                "Composer": "Bono/Clayton, Adam/Dylan, Bob/Mullen Jr., Larry/The Edge"
            },
            {
                "Name": "Love, Hate, Love",
                "Composer": "Jerry Cantrell, Layne Staley"
            },
            {
                "Name": "Loverman",
                "Composer": "Cave"
            },
            {
                "Name": "Loves Been Good To Me",
                "Composer": "rod mckuen"
            },
            {
                "Name": "Luminous Times (Hold On To Love)",
                "Composer": "Brian Eno/U2"
            },
            {
                "Name": "Make Love Like A Man",
                "Composer": None
            },
            {
                "Name": "May This Be Love",
                "Composer": "Jimi Hendrix"
            },
            {
                "Name": "My Love",
                "Composer": "Jauperi/Zeu Góes"
            },
            {
                "Name": "My Lovely Man",
                "Composer": "Anthony Kiedis/Chad Smith/Flea/John Frusciante"
            },
            {
                "Name": "New Love",
                "Composer": "Tim Maia"
            },
            {
                "Name": "Nothing But Love",
                "Composer": None
            },
            {
                "Name": "Oh, My Love",
                "Composer": None
            },
            {
                "Name": "Old Love",
                "Composer": "Eric Clapton, Robert Cray"
            },
            {
                "Name": "Pride (In The Name Of Love)",
                "Composer": "Bono/Clayton, Adam/Mullen Jr., Larry/The Edge"
            },
            {
                "Name": "Pride (In The Name Of Love)",
                "Composer": "U2"
            },
            {
                "Name": "Real Love",
                "Composer": "Billy Corgan"
            },
            {
                "Name": "Real Love",
                "Composer": None
            },
            {
                "Name": "Rhythm of Love",
                "Composer": None
            },
            {
                "Name": "Rollover D.J.",
                "Composer": "C. Cester/N. Cester"
            },
            {
                "Name": "She Loves Me Not",
                "Composer": "Bill Gould/Mike Bordin/Mike Patton"
            },
            {
                "Name": "Somebody To Love",
                "Composer": "Mercury, Freddie"
            },
            {
                "Name": "Stand Inside Your Love",
                "Composer": "Billy Corgan"
            },
            {
                "Name": "Summer Love",
                "Composer": "hans bradtke/heinz meier/johnny mercer"
            },
            {
                "Name": "Sunshine Of Your Love",
                "Composer": "Bruce/Clapton"
            },
            {
                "Name": "Talk About Love",
                "Composer": "roger glover"
            },
            {
                "Name": "The Deeper The Love",
                "Composer": "Vandenberg"
            },
            {
                "Name": "The Girl I Love She Got Long Black Wavy Hair",
                "Composer": "Jimmy Page/John Bonham/John Estes/John Paul Jones/Robert Plant"
            },
            {
                "Name": "The One I Love",
                "Composer": "R.E.M."
            },
            {
                "Name": "The Thin Line Between Love & Hate",
                "Composer": "David Murray/Steve Harris"
            },
            {
                "Name": "This Velvet Glove",
                "Composer": "Red Hot Chili Peppers"
            },
            {
                "Name": "Too Fast For Love",
                "Composer": "Nikki Sixx"
            },
            {
                "Name": "Turbo Lover",
                "Composer": None
            },
            {
                "Name": "Um Love",
                "Composer": None
            },
            {
                "Name": "Underwater Love",
                "Composer": "Faith No More"
            },
            {
                "Name": "Wasting Love",
                "Composer": "Bruce Dickinson/Janick Gers"
            },
            {
                "Name": "Wasting Love",
                "Composer": "Bruce Dickinson/Janick Gers"
            },
            {
                "Name": "Wasting Love",
                "Composer": None
            },
            {
                "Name": "What Now My Love",
                "Composer": "carl sigman/gilbert becaud/pierre leroyer"
            },
            {
                "Name": "When I Had Your Love",
                "Composer": "Robert Rogers/Warren \"Pete\" Moore/William \"Mickey\" Stevenson"
            },
            {
                "Name": "When It's Love",
                "Composer": "Edward Van Halen, Alex Van Halen, Michael Anthony,/Edward Van Halen, Alex Van Halen, Michael Anthony, Sammy Hagar"
            },
            {
                "Name": "When Love & Hate Collide",
                "Composer": None
            },
            {
                "Name": "When Love Comes To Town",
                "Composer": "Bono/Clayton, Adam/Mullen Jr., Larry/The Edge"
            },
            {
                "Name": "When Love Comes To Town",
                "Composer": "U2"
            },
            {
                "Name": "Whole Lotta Love",
                "Composer": "Jimmy Page/John Bonham/John Paul Jones/Robert Plant/Willie Dixon"
            },
            {
                "Name": "Whole Lotta Love",
                "Composer": "Jimmy Page, Robert Plant, John Paul Jones, John Bonham"
            },
            {
                "Name": "Whole Lotta Love",
                "Composer": "John Bonham/John Paul Jones/Robert Plant/Willie Dixon"
            },
            {
                "Name": "Whole Lotta Love (Medley)",
                "Composer": "Arthur Crudup/Bernard Besman/Bukka White/Doc Pomus/John Bonham/John Lee Hooker/John Paul Jones/Mort Shuman/Robert Plant/Willie Dixon"
            },
            {
                "Name": "Why Can't This Be Love",
                "Composer": "Van Halen"
            },
            {
                "Name": "You Can't Do it Right (With the One You Love)",
                "Composer": "D.Coverdale/G.Hughes/Glenn Hughes/R.Blackmore/Ritchie Blackmore"
            },
            {
                "Name": "You Sure Love To Ball",
                "Composer": "Marvin Gaye"
            }
        ],
        "category": "string_filtering",
    },
    {
        "question": "What is the average track length in minutes for each genre?",
        "sql": "SELECT g.Name, ROUND(AVG(t.Milliseconds) / 60000.0, 2) as AvgMinutes FROM Genre g JOIN Track t ON g.GenreId = t.GenreId GROUP BY g.GenreId, g.Name ORDER BY AvgMinutes DESC",
        "expected_result": [
            {
                "Name": "Sci Fi & Fantasy",
                "AvgMinutes": 48.53
            },
            {
                "Name": "Science Fiction",
                "AvgMinutes": 43.76
            },
            {
                "Name": "Drama",
                "AvgMinutes": 42.92
            },
            {
                "Name": "TV Shows",
                "AvgMinutes": 35.75
            },
            {
                "Name": "Comedy",
                "AvgMinutes": 26.42
            },
            {
                "Name": "Metal",
                "AvgMinutes": 5.16
            },
            {
                "Name": "Electronica/Dance",
                "AvgMinutes": 5.05
            },
            {
                "Name": "Heavy Metal",
                "AvgMinutes": 4.96
            },
            {
                "Name": "Classical",
                "AvgMinutes": 4.9
            },
            {
                "Name": "Jazz",
                "AvgMinutes": 4.86
            },
            {
                "Name": "Rock",
                "AvgMinutes": 4.73
            },
            {
                "Name": "Blues",
                "AvgMinutes": 4.51
            },
            {
                "Name": "Alternative",
                "AvgMinutes": 4.4
            },
            {
                "Name": "Reggae",
                "AvgMinutes": 4.12
            },
            {
                "Name": "Soundtrack",
                "AvgMinutes": 4.07
            },
            {
                "Name": "Alternative & Punk",
                "AvgMinutes": 3.91
            },
            {
                "Name": "Latin",
                "AvgMinutes": 3.88
            },
            {
                "Name": "Pop",
                "AvgMinutes": 3.82
            },
            {
                "Name": "World",
                "AvgMinutes": 3.75
            },
            {
                "Name": "R&B/Soul",
                "AvgMinutes": 3.67
            },
            {
                "Name": "Bossa Nova",
                "AvgMinutes": 3.66
            },
            {
                "Name": "Easy Listening",
                "AvgMinutes": 3.15
            },
            {
                "Name": "Hip Hop/Rap",
                "AvgMinutes": 2.97
            },
            {
                "Name": "Opera",
                "AvgMinutes": 2.91
            },
            {
                "Name": "Rock And Roll",
                "AvgMinutes": 2.24
            }
        ],
        "category": "aggregation_with_calculation",
    },
]
