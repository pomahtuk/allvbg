# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from images.models import AttachedImage
from geosite.models import Firm

def save_new_photo(single_firm, single_firm_photo):
    current_file = single_firm_photo.file
    new_photo = AttachedImage(order=0)
    new_photo.save()
    single_firm.images.add(new_photo)
    new_photo.photo.save(current_file.name, current_file)


class Command(BaseCommand):
    help = 'Migrates old allvbg data to new one, in this case - images'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        all_firms = Firm.objects.all()
        for single_firm in all_firms:
            # update images
            try:
                save_new_photo(single_firm, single_firm.image1)
                save_new_photo(single_firm, single_firm.image2)
                save_new_photo(single_firm, single_firm.image3)
                save_new_photo(single_firm, single_firm.image4)
            except ValueError:
                self.stdout.write('No image attached to %s' % single_firm.name)
            except IOError:
                self.stdout.write('Not an image for firm %s' % single_firm.name)
            finally:
                self.stdout.write('Successfully created photos for firm %s' % single_firm.name)
        self.stdout.write('Successfully executed command')
