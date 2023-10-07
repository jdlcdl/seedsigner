from base import FlowTest, FlowStep

from seedsigner.controller import Controller
from seedsigner.views.view import MainMenuView
from seedsigner.views import scan_views, seed_views, psbt_views

class TestPSBTFlows(FlowTest):

	def test_scan_psbt_first_then_correct_seedqr_flow(self):
		"""
			Selecting "Scan" from the MainMenuView and scanning a PSBT should enter the PSBTSelectSeedView flow
			when Scan a Seed is selected from PSBTSelectSeedView it should enter the ScanView flow
			when a SeedQR is scanned it should enter the PSBTOverviewView flow
			since the PSBT has change no warning is displayed and it should enter the PSBTMathView flow
			since the PSBT is not a self transfer it should enter the PSBTAddressDetailsView flow
		"""
		def load_psbt_into_decoder(view: scan_views.ScanView):
			"""
				PSBT Tx and Wallet Details
				- Single Sig Wallet P2WPKH (Native Segwit) with no passphrase
				- Regtest c751dc07 m/84'/1'/0' tpubDDZBrnxMxbVzqt8EoEiABPxeKzFWma5pra5UEbg3Wst1hrwr6feuvcy7Sov7cpuYx94ypuy1PQ9NDNoQagFs37wGALzLb5Ei3FvyJWPPPKZ
				- 2 Inputs
					- 56,522,834 sats
					- 1,990,245,069 sats
				- 4 Outputs
					- 1 Output to another wallet (bcrt1q7cw0wzy8g6mq5qvkpvhnk5gsps5ncy3srp0n2j) of 123,456 sats
					- 3 Outputs change
						- 3 outputs to emulate a fake mix to increase privacy
						- Change addresses are index 1/7, 1/8, 1/9
						- 1/7 address bcrt1q53j0xwuskuf5gnvynadh0hlazyy8srydlucrhg with amount 123,456 sats
						- 1/8 address bcrt1q5gtw3zfp4cx67yk5q42q6j6rfza8aqcwpyyslv with amount 1,990,121,477 sats
						- 1/9 address bcrt1q9rrg7399m43cn0yg4tz0v0ate89jgf2d6kpz7v with amount 56,399,242 sats
					- Fee 272 sats
			"""
			view.decoder.add_data("cHNidP8BANgCAAAAAsTXZs3fz/dmGb6M80+jjvJZdYya+cw5bT/dGuhZFdSlAAAAAAD9////qo6xg/UZAvUkcbse1F+C9zbP/FeZNjThx7SCIn6eMCgBAAAAAP3///8EQOIBAAAAAAAWABSkZPM7kLcTRE2En1t33/0RCHgMjQXYnnYAAAAAFgAUKMaPRKXdY4m8iKrE9j+rycskJU1A4gEAAAAAABYAFPYc9wiHRrYKAZYLLztREAwpPBIwipVcAwAAAAAWABSiFuiJIa4NrxLUBVQNS0NIun6DDtoRAABPAQQ1h88DBcQGZIAAAAA+0J+jlNL3dpWwlnBi8Dx+Ipg4e6uvB3HdjzFPX7r9CAOOlAIxgII+/xCcj+XoEenKH7wj5s5wlu7Q7CCZWFLGLhA5Su0UVAAAgAEAAIAAAACAAAEA7QIAAAAEE6njX/fnvn7hbkKIRcxzNYFOSfbCdNeWnd7Fe/1UcQ0BAAAAAP3///8TqeNf9+e+fuFuQohFzHM1gU5J9sJ015ad3sV7/VRxDQMAAAAA/f///xOp41/3575+4W5CiEXMczWBTkn2wnTXlp3exXv9VHENBAAAAAD9////E6njX/fnvn7hbkKIRcxzNYFOSfbCdNeWnd7Fe/1UcQ0GAAAAAP3///8CUnheAwAAAAAWABRCfygPJ+Fjsx4BknYvvm3A3qKn2xJ/XQcAAAAAF6kU1I4TAst5nAj15ey7vwe5cM3OFq+HlhEAAAEBH1J4XgMAAAAAFgAUQn8oDyfhY7MeAZJ2L75twN6ip9sBAwQBAAAAIgYCo7sfm78RQY3B5n0ac/QF8VtMAzFnci+h5D1MtpgRY7oYOUrtFFQAAIABAACAAAAAgAEAAAAGAAAAAAEAcQIAAAABxY7wh0nsfJQfzWrD/9rN9BYsM+iOmPaO6I0ANFgO/PcAAAAAAP3///8CptiUAAAAAAAWABRIm4HhQY/TzOjeWSPRrbuJo9MlW826oHYAAAAAFgAU0z+0L2QSLGtyQTn8FhbCpcI7jbliAQAAAQEfzbqgdgAAAAAWABTTP7QvZBIsa3JBOfwWFsKlwjuNuQEDBAEAAAAiBgITHmebEANk81CraV4xZIpqkNjjw0tIvezl1Ism1NRH3Rg5Su0UVAAAgAEAAIAAAACAAQAAAAAAAAAAIgICuTT7WnuiUTpObjWnZFHzIeEvW9PTB+1LLVFNQJVFeIIYOUrtFFQAAIABAACAAAAAgAEAAAAHAAAAACICAk8f3hpc5C35chgSg+Pe2zZ9IhHREd4aKW2+yAMRIFeqGDlK7RRUAACAAQAAgAAAAIABAAAACQAAAAAAIgIDjt1CjvrnMMnjbmTNKUAYoKEDRbmKjNjbq+6Ppqj3bqQYOUrtFFQAAIABAACAAAAAgAEAAAAIAAAAAA==")

		def load_seed_into_decoder(view: scan_views.ScanView):
			view.decoder.add_data("080115060387063104071857067618681125136207731354")
	
		self.run_sequence([
			FlowStep(MainMenuView, button_data_selection=MainMenuView.SCAN),
			FlowStep(scan_views.ScanView, before_run=load_psbt_into_decoder),  # simulate read PSBT; ret val is ignored
			FlowStep(psbt_views.PSBTSelectSeedView, button_data_selection=psbt_views.PSBTSelectSeedView.SCAN_SEED),
			FlowStep(scan_views.ScanSeedQRView, before_run=load_seed_into_decoder),
			FlowStep(seed_views.SeedFinalizeView, button_data_selection=seed_views.SeedFinalizeView.FINALIZE),
			FlowStep(seed_views.SeedOptionsView, is_redirect=True),
			FlowStep(psbt_views.PSBTOverviewView),
			FlowStep(psbt_views.PSBTMathView),
			FlowStep(psbt_views.PSBTAddressDetailsView, button_data_selection=0),
			FlowStep(psbt_views.PSBTChangeDetailsView, button_data_selection=psbt_views.PSBTChangeDetailsView.NEXT),
			FlowStep(psbt_views.PSBTChangeDetailsView, button_data_selection=psbt_views.PSBTChangeDetailsView.NEXT),
			FlowStep(psbt_views.PSBTChangeDetailsView, button_data_selection=psbt_views.PSBTChangeDetailsView.NEXT),
			FlowStep(psbt_views.PSBTFinalizeView, button_data_selection=psbt_views.PSBTFinalizeView.APPROVE_PSBT),
			FlowStep(psbt_views.PSBTSignedQRDisplayView),
			FlowStep(MainMenuView)
		])
		
	def test_scan_multisig_psbt_seed_already_signed_flow(self):
		
		def load_psbt_into_decoder(view: scan_views.ScanView):
			view.decoder.add_data("cHNidP8BAIkCAAAAAc9dCSh2RcRPfHaT5bNVBpbg0jAekRLqOK+bpN/QA0jeAAAAAAD9////AtAHAAAAAAAAIlEg24shYsV3IRCzlgmMKjAsR4Ad9tX896z7zDAi5q0TU9H3CgAAAAAAACIAIByGQg/VP2aRID62ty40E64HYZeRRsKRGLt8J/76R6stQ04FAE8BBDWHzwSLLGdzgAAAAq3q6nR20JnHR+vKrBQdWxN9C7xU8zNX942mVF7AQpl2ArrdLwVlkGxaatQJ4wwkvypNBKbwOq9hXGLNlKi7rZWAFDUxzXUwAACAAQAAgAAAAIACAACATwEENYfPBHOCZmWAAAACmH6KTXIny0vueRgQFBq4M6oMuG8f1QM0I/RzKQ03bCgCHrF0fyUtV0+FD2N34u/woqb8MAt/o+7Ed58RddhY8zYUCUjSaDAAAIABAACAAAAAgAIAAIAAAQEriBMAAAAAAAAiACBY4WsjDgJXLj3VW222jU1tkIIhT26ce/2efH73BWGGBiICAqyfkrdUO662QBrdvJcSOZMFxniD7M1awm9U0Kb5XCm5RzBEAiAPkQTY84YjFFkpD6MI2cc5rJySqws5fsTQA/8XEZFpbAIgTNVykbEH4Z7bqyzhhy6lty0K8rtCUDCaHNv+47NNIWgBAQMEAQAAAAEFR1IhApL4XO+VE1pPYn5wnRFyJQKVSc9TX2dO6KIBH6jwvgPaIQKsn5K3VDuutkAa3byXEjmTBcZ4g+zNWsJvVNCm+VwpuVKuIgYCkvhc75UTWk9ifnCdEXIlApVJz1NfZ07oogEfqPC+A9ocNTHNdTAAAIABAACAAAAAgAIAAIAAAAAAAAAAACIGAqyfkrdUO662QBrdvJcSOZMFxniD7M1awm9U0Kb5XCm5HAlI0mgwAACAAQAAgAAAAIACAACAAAAAAAAAAAAAAAEBR1IhApYXaczuYbBM/A+EH639Ir2yIB4PxL46dK/I1V1O9aHgIQLa02HCI/+EP+9gGpxHskjYWFN5hZzXY7RRvwV4UF42ylKuIgIClhdpzO5hsEz8D4Qfrf0ivbIgHg/Evjp0r8jVXU71oeAcNTHNdTAAAIABAACAAAAAgAIAAIABAAAAAAAAACICAtrTYcIj/4Q/72AanEeySNhYU3mFnNdjtFG/BXhQXjbKHAlI0mgwAACAAQAAgAAAAIACAACAAQAAAAAAAAAA")
		
		def load_seed_into_decoder(view: scan_views.ScanView):
			view.decoder.add_data("073318950739065415961602009907670428187212261116")
			
		self.run_sequence([
			FlowStep(MainMenuView, button_data_selection=MainMenuView.SCAN),
			FlowStep(scan_views.ScanView, before_run=load_psbt_into_decoder),  # simulate read PSBT; ret val is ignored
			FlowStep(psbt_views.PSBTSelectSeedView, button_data_selection=psbt_views.PSBTSelectSeedView.SCAN_SEED),
			FlowStep(scan_views.ScanSeedQRView, before_run=load_seed_into_decoder),
			FlowStep(seed_views.SeedFinalizeView, button_data_selection=seed_views.SeedFinalizeView.FINALIZE),
			FlowStep(seed_views.SeedOptionsView, is_redirect=True),
			FlowStep(psbt_views.PSBTOverviewView),
			FlowStep(psbt_views.PSBTMathView),
			FlowStep(psbt_views.PSBTAddressDetailsView, button_data_selection=0),
			FlowStep(psbt_views.PSBTChangeDetailsView, button_data_selection=psbt_views.PSBTChangeDetailsView.NEXT),
			FlowStep(psbt_views.PSBTFinalizeView, button_data_selection=psbt_views.PSBTFinalizeView.APPROVE_PSBT),
			FlowStep(psbt_views.PSBTSigningErrorView, button_data_selection=psbt_views.PSBTSigningErrorView.SELECT_DIFF_SEED),
			FlowStep(psbt_views.PSBTSelectSeedView, button_data_selection=psbt_views.PSBTSelectSeedView.SCAN_SEED),
			FlowStep(scan_views.ScanSeedQRView, before_run=load_seed_into_decoder),
			FlowStep(seed_views.SeedFinalizeView, button_data_selection=seed_views.SeedFinalizeView.PASSPHRASE),
			FlowStep(seed_views.SeedAddPassphraseView, screen_return_value="abc"),
			FlowStep(seed_views.SeedReviewPassphraseView, button_data_selection=seed_views.SeedReviewPassphraseView.DONE),
			FlowStep(seed_views.SeedOptionsView, is_redirect=True),
			FlowStep(psbt_views.PSBTOverviewView),
			FlowStep(psbt_views.PSBTMathView),
			FlowStep(psbt_views.PSBTAddressDetailsView, button_data_selection=0),
			FlowStep(psbt_views.PSBTChangeDetailsView, button_data_selection=psbt_views.PSBTChangeDetailsView.NEXT),
			FlowStep(psbt_views.PSBTFinalizeView, button_data_selection=psbt_views.PSBTFinalizeView.APPROVE_PSBT),
			FlowStep(psbt_views.PSBTSignedQRDisplayView),
			FlowStep(MainMenuView),
		])
		
